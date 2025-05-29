#!/bin/bash

# --- Configuration ---
if [ -z "$1" ]; then read -p "Enter the TARGET VPC ID: " TARGET_VPC_ID; else TARGET_VPC_ID=$1; fi
if [ -z "$TARGET_VPC_ID" ]; then echo "ERROR: Target VPC ID is required."; exit 1; fi

if [ -z "$2" ]; then
    DEFAULT_INPUT_FILE_GUESS="source_vpc_*_sgs_details.json"
    FOUND_FILES=( $(ls -1 ${DEFAULT_INPUT_FILE_GUESS} 2>/dev/null) )
    if [ ${#FOUND_FILES[@]} -eq 1 ]; then
        echo "Found one potential input file: ${FOUND_FILES[0]}"
        read -p "Use this file? (Y/n): " use_found_file
        if [[ "$use_found_file" =~ ^[Yy]([Ee][Ss])?$|^$ ]]; then
             INPUT_FILE="${FOUND_FILES[0]}"
        fi
    fi
    if [ -z "$INPUT_FILE" ]; then
        read -p "Enter the path to the SOURCE Security Group details JSON file: " INPUT_FILE
    fi
else
    INPUT_FILE=$2
fi

if [ -z "$INPUT_FILE" ] || [ ! -f "$INPUT_FILE" ]; then
    echo "ERROR: Input JSON file '${INPUT_FILE}' not found or not specified."
    exit 1
fi

MAPPING_FILE="sg_id_mapping_vpc_${TARGET_VPC_ID}.txt"
SG_ID_MAP_JSON_FILE="sg_id_map_vpc_${TARGET_VPC_ID}.json"

# --- Main Logic ---
echo "---------------------------------------------------------------------"
echo "IMPORTING SECURITY GROUPS TO TARGET ACCOUNT (WITH RULE REPLACEMENT FOR EXISTING SGs)"
echo "Ensure your AWS CLI is currently configured for the TARGET account."
echo "Target VPC ID: ${TARGET_VPC_ID}"
echo "Reading source SG details from: ${INPUT_FILE}"
echo "SG ID mapping will be saved to: ${MAPPING_FILE} and ${SG_ID_MAP_JSON_FILE}"
echo "Press Enter to continue or Ctrl+C to abort..."
read -r

> "${MAPPING_FILE}" # Initialize MAPPING_FILE: ensure it's empty or create it

# --- First Pass: Create/Identify Security Groups in Target VPC ---
echo "Processing Security Groups in target VPC ${TARGET_VPC_ID}..."
jq -c '.SecurityGroups[]' "${INPUT_FILE}" | while IFS= read -r sg_json; do
    group_name=$(echo "$sg_json" | jq -r '.GroupName')
    description=$(echo "$sg_json" | jq -r '.Description')
    source_group_id=$(echo "$sg_json" | jq -r '.GroupId | select(.!=null and .!="")')

    if [[ -z "$source_group_id" ]]; then
        echo "Warning: Found an SG in source JSON with no GroupId or empty GroupId. Skipping."
        continue
    fi

    if [[ "$group_name" == "default" ]]; then
        echo "Ignoring source default SG named 'default' (ID: $source_group_id)."
        continue
    fi

    sg_exists_in_target="false"
    target_sg_id_to_map=""

    existing_sg_details_json=$(aws ec2 describe-security-groups --filters Name=vpc-id,Values=${TARGET_VPC_ID} Name=group-name,Values="${group_name}" --output json 2>/dev/null)
    existing_sg_id=$(echo "$existing_sg_details_json" | jq -r '.SecurityGroups[0].GroupId // ""')

    if [[ -n "$existing_sg_id" ]]; then
        echo "SG '${group_name}' (Source ID: ${source_group_id}) already exists in target VPC with ID: ${existing_sg_id}."
        target_sg_id_to_map="${existing_sg_id}"
        sg_exists_in_target="true"

        existing_ingress_rules=$(echo "$existing_sg_details_json" | jq -c '.SecurityGroups[0].IpPermissions // []')
        existing_egress_rules=$(echo "$existing_sg_details_json" | jq -c '.SecurityGroups[0].IpPermissionsEgress // []')

        if [[ "$group_name" != "default" ]]; then
            if [[ "$existing_ingress_rules" != "[]" && "$existing_ingress_rules" != "null" ]]; then
                echo "  Revoking existing INGRESS rules from ${existing_sg_id}..."
                aws ec2 revoke-security-group-ingress --group-id "${existing_sg_id}" --ip-permissions "${existing_ingress_rules}" >/dev/null 2>&1
            fi
            if [[ "$existing_egress_rules" != "[]" && "$existing_egress_rules" != "null" ]]; then
                echo "  Revoking existing EGRESS rules from ${existing_sg_id}..."
                aws ec2 revoke-security-group-egress --group-id "${existing_sg_id}" --ip-permissions "${existing_egress_rules}" >/dev/null 2>&1
            fi
        else
            echo "  Skipping rule revocation for SG named 'default' (${existing_sg_id}) in target VPC."
        fi
    else
        echo "Attempting to create SG: Name='${group_name}', Description='${description}' in VPC ${TARGET_VPC_ID}"
        create_output=$(aws ec2 create-security-group \
            --group-name "${group_name}" \
            --description "${description}" \
            --vpc-id "${TARGET_VPC_ID}" \
            --output json)

        if [ $? -ne 0 ]; then
            echo "ERROR creating security group ${group_name}. Output: ${create_output}"
            continue
        fi
        new_group_id=$(echo "$create_output" | jq -r '.GroupId // ""')
        if [[ -z "$new_group_id" ]]; then
            echo "ERROR: Could not get new GroupId for ${group_name} after creation. Output: ${create_output}"
            continue
        fi
        echo "Created SG ${group_name} with new ID: ${new_group_id}"
        target_sg_id_to_map="${new_group_id}"

        original_tags_json=$(echo "$sg_json" | jq -c '.Tags | select(.!=null and .!=[])')
        if [[ -n "$original_tags_json" && "$original_tags_json" != "null" && "$original_tags_json" != "[]" ]]; then
            transformed_tags_json=$(echo "$original_tags_json" | jq -c 'map(if .Key | startswith("aws:") then { "Key": (.Key | sub("aws:"; "migrated_aws_")), "Value": .Value } else . end)')
            final_tags_to_apply_json=$(echo "$transformed_tags_json" | jq -c 'map(select(.Key != "" and .Key != null))')
            if [[ -n "$final_tags_to_apply_json" && "$final_tags_to_apply_json" != "null" && "$final_tags_to_apply_json" != "[]" ]]; then
                echo "Adding transformed tags to NEWLY CREATED ${new_group_id}: ${final_tags_to_apply_json}"
                aws ec2 create-tags --resources "${new_group_id}" --tags "${final_tags_to_apply_json}"
                if [ $? -ne 0 ]; then echo "ERROR adding tags to ${new_group_id}."; fi
            fi
        fi
    fi

    if [[ -n "$target_sg_id_to_map" ]]; then
        echo "${source_group_id}=${target_sg_id_to_map}" >> "${MAPPING_FILE}"
    else
        echo "Warning: No target SG ID determined for source SG ${source_group_id} ('${group_name}'). Not adding to mapping."
    fi
done

echo "SG ID Mapping generation complete. Contents of ${MAPPING_FILE}:"
cat "${MAPPING_FILE}"

# Create a JSON version of the mapping for easier use in later jq commands
if [ -s "${MAPPING_FILE}" ]; then
    # Ensure only valid lines are processed and build the JSON object
    # Valid line: contains '=', first part not empty, second part not empty
    jq -Rn 'reduce (inputs | select(test("=") and split("=")[0] != "" and split("=")[1] != "") | split("=")) as $kv ({}; .[$kv[0]] = $kv[1])' "${MAPPING_FILE}" > "${SG_ID_MAP_JSON_FILE}"

    if [ $? -ne 0 ] || ! jq -e . "${SG_ID_MAP_JSON_FILE}" > /dev/null 2>&1 ; then # Check if jq errored or output is not valid JSON
        echo "ERROR: Failed to create valid JSON mapping file ${SG_ID_MAP_JSON_FILE} from ${MAPPING_FILE}."
        echo "Contents of ${MAPPING_FILE} that was processed:"
        cat "${MAPPING_FILE}" # Show raw mapping file for debug
        echo "Attempted JSON output (may be incomplete or invalid):"
        cat "${SG_ID_MAP_JSON_FILE}"
        exit 1
    fi
else
    echo "{}" > "${SG_ID_MAP_JSON_FILE}" # Create an empty JSON object if MAPPING_FILE is empty
fi


if [ ! -s "${SG_ID_MAP_JSON_FILE}" ] && [ -s "${MAPPING_FILE}" ]; then
    # This case should ideally be caught by the error check above
    echo "ERROR: JSON mapping file ${SG_ID_MAP_JSON_FILE} is empty but text mapping file ${MAPPING_FILE} is not."
    exit 1
elif [ ! -s "${SG_ID_MAP_JSON_FILE}" ] && [ ! -s "${MAPPING_FILE}" ]; then
    echo "Warning: Both mapping files are empty. This is normal if only default SGs were in the source or all failed."
fi

echo "Sleeping for rule processing..."
sleep 10

# --- Second Pass: Add Ingress and Egress Rules (Now to potentially cleared SGs) ---
echo "Adding rules to Security Groups..."
jq -c '.SecurityGroups[]' "${INPUT_FILE}" | while IFS= read -r sg_json; do
    source_group_id=$(echo "$sg_json" | jq -r '.GroupId | select(.!=null and .!="")')
    source_group_name=$(echo "$sg_json" | jq -r '.GroupName')

    if [[ -z "$source_group_id" ]]; then
        continue
    fi

    if [[ "$source_group_name" == "default" ]]; then
        echo "Skipping rule processing for ignored source default SG ${source_group_name}."
        continue
    fi

    target_sg_id_for_rules=$(jq -r --arg key "$source_group_id" '.[$key] // ""' "${SG_ID_MAP_JSON_FILE}")
    if [[ -z "$target_sg_id_for_rules" ]]; then
        echo "Skipping rules for source SG ${source_group_name} (ID: ${source_group_id}) as it's not in the final JSON map (${SG_ID_MAP_JSON_FILE})."
        continue
    fi

    echo "Processing rules for source SG ${source_group_name} (${source_group_id}) -> target SG ID ${target_sg_id_for_rules}"

    # --- Process Ingress Rules ---
    ip_permissions_raw=$(echo "$sg_json" | jq -c '.IpPermissions | select(.!=null)')

    if [[ -n "$ip_permissions_raw" && "$ip_permissions_raw" != "null" && "$ip_permissions_raw" != "[]" ]]; then
        transformed_ingress_rules=$(echo "$ip_permissions_raw" | jq -c --slurpfile idmap "${SG_ID_MAP_JSON_FILE}" --arg current_target_id "$target_sg_id_for_rules" --arg current_source_id "$source_group_id" '
            map(
                . as $permission_obj |
                $permission_obj + {
                    "UserIdGroupPairs": [
                        ($permission_obj.UserIdGroupPairs[]? |
                            (.) as $originalPair |
                            if .GroupId == $current_source_id then
                                { "GroupId": $current_target_id }
                                + (if $originalPair.Description then {"Description": $originalPair.Description} else {} end)
                                + (if $originalPair.UserId and $originalPair.UserId != "" and $originalPair.UserId != null then {"UserId": $originalPair.UserId} else {} end)
                            elif $idmap[0]?[$originalPair.GroupId] then
                                { "GroupId": $idmap[0][$originalPair.GroupId] }
                                + (if $originalPair.Description then {"Description": $originalPair.Description} else {} end)
                                + (if $originalPair.UserId and $originalPair.UserId != "" and $originalPair.UserId != null then {"UserId": $originalPair.UserId} else {} end)
                            else
                                empty
                            end
                        )
                    ]
                } |
                .IpRanges |= (. // []) |
                .Ipv6Ranges |= (. // []) |
                .PrefixListIds |= (. // [])
            ) |
            map(select(
                (.IpRanges | length > 0) or
                (.Ipv6Ranges | length > 0) or
                (.PrefixListIds | length > 0) or
                (.UserIdGroupPairs | length > 0)
            ))
        ')

        if [[ -n "$transformed_ingress_rules" && "$transformed_ingress_rules" != "[]" && "$transformed_ingress_rules" != "null" ]]; then
            echo "  Authorizing Ingress for ${target_sg_id_for_rules} with rules: ${transformed_ingress_rules}"
            aws ec2 authorize-security-group-ingress --group-id "${target_sg_id_for_rules}" --ip-permissions "${transformed_ingress_rules}"
            if [ $? -ne 0 ]; then echo "  ERROR authorizing ingress."; else echo "  Ingress authorized."; fi
        else echo "  No valid ingress rules to apply after transformation."; fi
    else echo "  No source ingress rules for SG ${source_group_name}."; fi


    # --- Process Egress Rules ---
    ip_permissions_egress_raw=$(echo "$sg_json" | jq -c '.IpPermissionsEgress | select(.!=null)')
    is_standard_allow_all_egress="false"
    if [[ $(echo "$ip_permissions_egress_raw" | jq -c --raw-output 'if . == null then "false" else (length == 1 and (.[0].IpProtocol == "-1" or (.[0].IpProtocol == "all" and .[0].FromPort == 0 and .[0].ToPort == 65535)) and (.[0].IpRanges | length == 1 and .[0].IpRanges[0].CidrIp == "0.0.0.0/0") and (.[0].Ipv6Ranges | length == 0 or .[0].Ipv6Ranges == null) and (.[0].PrefixListIds | length == 0 or .[0].PrefixListIds == null) and (.[0].UserIdGroupPairs | length == 0 or .[0].UserIdGroupPairs == null)) end' | tr '[:upper:]' '[:lower:]') == "true" ]]; then
        is_standard_allow_all_egress="true"
    fi

    if [[ "$is_standard_allow_all_egress" == "true" ]]; then
        echo "  Source SG ${source_group_name} had standard 'Allow All' egress. Ensuring target SG ${target_sg_id_for_rules} has it."
        target_sg_name_check=$(aws ec2 describe-security-groups --group-ids "${target_sg_id_for_rules}" --query "SecurityGroups[0].GroupName" --output text 2>/dev/null)
        if [[ "$target_sg_name_check" != "default" ]]; then
            current_target_egress=$(aws ec2 describe-security-groups --group-ids "${target_sg_id_for_rules}" --query "SecurityGroups[0].IpPermissionsEgress" --output json 2>/dev/null)
            has_allow_all_already=$(echo "$current_target_egress" | jq -c --raw-output 'if . == null then "false" else (length == 1 and (.[0].IpProtocol == "-1" or (.[0].IpProtocol == "all" and .[0].FromPort == 0 and .[0].ToPort == 65535)) and (.[0].IpRanges | length == 1 and .[0].IpRanges[0].CidrIp == "0.0.0.0/0") and (.[0].Ipv6Ranges | length == 0 or .[0].Ipv6Ranges == null) and (.[0].PrefixListIds | length == 0 or .[0].PrefixListIds == null) and (.[0].UserIdGroupPairs | length == 0 or .[0].UserIdGroupPairs == null)) end' | tr '[:upper:]' '[:lower:]')
            if [[ "$has_allow_all_already" == "false" ]]; then
                 echo "    Target SG ${target_sg_id_for_rules} does not have allow-all egress, adding it."
                 default_egress_rule='[{"IpProtocol": "-1", "IpRanges": [{"CidrIp": "0.0.0.0/0"}]}]'
                 aws ec2 authorize-security-group-egress --group-id "${target_sg_id_for_rules}" --ip-permissions "${default_egress_rule}" >/dev/null 2>&1
            else
                 echo "    Target SG ${target_sg_id_for_rules} already has allow-all egress."
            fi
        fi
    elif [[ -n "$ip_permissions_egress_raw" && "$ip_permissions_egress_raw" != "null" && "$ip_permissions_egress_raw" != "[]" ]]; then
        transformed_egress_rules=$(echo "$ip_permissions_egress_raw" | jq -c --slurpfile idmap "${SG_ID_MAP_JSON_FILE}" --arg current_target_id "$target_sg_id_for_rules" --arg current_source_id "$source_group_id" '
            map(
                . as $permission_obj |
                $permission_obj + {
                    "UserIdGroupPairs": [
                        ($permission_obj.UserIdGroupPairs[]? |
                            (.) as $originalPair |
                            if .GroupId == $current_source_id then
                                { "GroupId": $current_target_id }
                                + (if $originalPair.Description then {"Description": $originalPair.Description} else {} end)
                                + (if $originalPair.UserId and $originalPair.UserId != "" and $originalPair.UserId != null then {"UserId": $originalPair.UserId} else {} end)
                            elif $idmap[0]?[$originalPair.GroupId] then
                                { "GroupId": $idmap[0][$originalPair.GroupId] }
                                + (if $originalPair.Description then {"Description": $originalPair.Description} else {} end)
                                + (if $originalPair.UserId and $originalPair.UserId != "" and $originalPair.UserId != null then {"UserId": $originalPair.UserId} else {} end)
                            else
                                empty
                            end
                        )
                    ]
                } |
                .IpRanges |= (. // []) |
                .Ipv6Ranges |= (. // []) |
                .PrefixListIds |= (. // [])
            ) |
            map(select(
                (.IpRanges | length > 0) or
                (.Ipv6Ranges | length > 0) or
                (.PrefixListIds | length > 0) or
                (.UserIdGroupPairs | length > 0)
            ))
        ')

        if [[ -n "$transformed_egress_rules" && "$transformed_egress_rules" != "[]" && "$transformed_egress_rules" != "null" ]]; then
            echo "  Authorizing Custom Egress for ${target_sg_id_for_rules}: ${transformed_egress_rules}"
            target_sg_name_check=$(aws ec2 describe-security-groups --group-ids "${target_sg_id_for_rules}" --query "SecurityGroups[0].GroupName" --output text 2>/dev/null)
            if [[ "$target_sg_name_check" != "default" ]]; then
                current_target_egress_for_new_sg_check=$(aws ec2 describe-security-groups --group-ids "${target_sg_id_for_rules}" --query "SecurityGroups[0].IpPermissionsEgress" --output json 2>/dev/null)
                is_current_target_allow_all=$(echo "$current_target_egress_for_new_sg_check" | jq -c --raw-output 'if . == null then "false" else (length == 1 and (.[0].IpProtocol == "-1" or (.[0].IpProtocol == "all" and .[0].FromPort == 0 and .[0].ToPort == 65535)) and (.[0].IpRanges | length == 1 and .[0].IpRanges[0].CidrIp == "0.0.0.0/0") and (.[0].Ipv6Ranges | length == 0 or .[0].Ipv6Ranges == null) and (.[0].PrefixListIds | length == 0 or .[0].PrefixListIds == null) and (.[0].UserIdGroupPairs | length == 0 or .[0].UserIdGroupPairs == null)) end' | tr '[:upper:]' '[:lower:]')
                if [[ "$is_current_target_allow_all" == "true" ]]; then
                    echo "    Revoking default 'Allow All' egress from SG ${target_sg_id_for_rules} before adding custom rules."
                    default_egress_rule_to_revoke='[{"IpProtocol": "-1", "IpRanges": [{"CidrIp": "0.0.0.0/0"}]}]'
                    aws ec2 revoke-security-group-egress --group-id "${target_sg_id_for_rules}" --ip-permissions "${default_egress_rule_to_revoke}" >/dev/null 2>&1
                fi
            fi
            aws ec2 authorize-security-group-egress --group-id "${target_sg_id_for_rules}" --ip-permissions "${transformed_egress_rules}"
            if [ $? -ne 0 ]; then echo "  ERROR authorizing egress."; else echo "  Egress authorized."; fi
        else echo "  No valid custom egress rules to apply after transformation."; fi
    else echo "  No source egress rules for SG ${source_group_name}."; fi
done

echo "---------------------------------------------------------------------"
echo "Security Group import process attempted. Please VERIFY THOROUGHLY."
echo "Check for any errors above and inspect the SGs manually or via AWS CLI."
echo "Mapping file: ${MAPPING_FILE}"
echo "JSON mapping file: ${SG_ID_MAP_JSON_FILE}"
echo "Source SG details were read from: ${INPUT_FILE}"
echo "---------------------------------------------------------------------"