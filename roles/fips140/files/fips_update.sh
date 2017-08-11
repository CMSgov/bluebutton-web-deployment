#!/usr/bin/env bash

# This script will help setup FIPS 140-2 support for an
# existing Redhat 7.x server. In our enviroment we do not
# have /boot on a separate file system. This simplifies
# some of the steps and this script does not even try
# to check and perform updates needed for a server with
# a separate /boot
#
# To complete the setup this script must be run 4 times as
# we have 4 reboots. Run the script as follows:
# ./fips_updates.ksh 1
# Server will reboot after pass 1 work is completed
# ./fips_updates.ksh 2
# Server will reboot after pass 2 work is completed
# ./fips_updates.ksh 3
# Server will reboot after pass 3 work is completed
# ./fips_updates.ksh 4
# Server will reboot after pass 4 work is completed

LOG_FILE='/root/fips_140_2_update.log'

if [ $# -ne 1 ]
  then
  echo "Usage: $0 <Pass Number>"
  exit 1
  fi

if [ $1 -eq 0 ]
  then
  echo "Initializing LogFile: $LOGFILE" > $LOG_FILE
  date >> $LOG_FILE
  echo "" >> $LOG_FILE
  exit 0
fi

if [ $1 -eq 1 ]
  then
  echo "Starting Pass 1" > $LOG_FILE
  date >> $LOG_FILE
  echo "" >> $LOG_FILE
  echo "Starting yum update now" >> $LOG_FILE
  yum -y update >> $LOG_FILE 2>&1
  echo "Rebooting now" >> $LOG_FILE
  echo "" >> $LOG_FILE
  # Call shutdown in Ansible after this script completes
  # shutdown -r now
  echo "step 1 completed" >>$LOG_FILE.1done
  exit 0
  fi

if [ $1 -eq 2 ]
  then
  echo "Starting Pass 2" >> $LOG_FILE
  date >> $LOG_FILE
  echo "" >> $LOG_FILE

# All of our servers have the AES-NI enhanced performance chips so I don't
# need this check. I never got it to log right so I'm just commenting it out
# but it does work correctly from the CLI
# echo "Check to see if the server supports AES-NI enhanced performance" >> $LOG_FILE
#  echo "grep -qw aes /proc/cpuinfo && echo YES || echo no" >> $LOG_FILE
#  grep -qw aes /proc/cpuinfo && echo YES || echo NO >> $LOG_FILE 2>&1
#  echo "" >> $LOG_FILE

  echo "yum install dracut-fips-aesni" >> $LOG_FILE
  yum install -y dracut-fips-aesni >> $LOG_FILE 2>&1
  echo "" >> $LOG_FILE
  echo "Checking to see if prelink package is installed." >> $LOG_FILE
  echo "rpm -q prelink" >> $LOG_FILE 2>&1
  rpm -q prelink >> $LOG_FILE 2>&1
  echo "" >> $LOG_FILE
  echo "Backing up existing initramfs" >> $LOG_FILE
  echo 'mv -vf /boot/initramfs-$(uname -r).img{,.bak}' >> $LOG_FILE
  mv -v /boot/initramfs-$(uname -r).img{,.bak} >> $LOG_FILE 2>&1
  echo "" >> $LOG_FILE
  echo "Run dracut to rebuild initramfs" >> $LOG_FILE
  echo "dracut --force " >> $LOG_FILE
  dracut --force >> $LOG_FILE 2>&1
  echo "" >> $LOG_FILE
  echo "Edit kernel command-line to include the fips=1 argument" >> $LOG_FILE
  echo "grubby --update-kernel=$(grubby --default-kernel) --args=fips=1" >> $LOG_FILE
  grubby --update-kernel=$(grubby --default-kernel) --args=fips=1
  echo "" >> $LOG_FILE
  echo "Rebooting now" >> $LOG_FILE
  echo "" >> $LOG_FILE
  # Call shutdown in Ansible after this script completes
  # shutdown -r now
  echo "step 2 completed" >>$LOG_FILE.2done
  exit 0
  fi

if [ $1 -eq 3 ]
  then
  echo "Starting Pass 3" >> $LOG_FILE
  date >> $LOG_FILE
  echo "" >> $LOG_FILE
  echo "Update GRUB_CMDLINE_LINUX" >> $LOG_FILE
  echo 'sed -i /^GRUB_CMDLINE_LINUX=/s/"$/ fips=1"/ /etc/default/grub' >> $LOG_FILE
  sed -i '/^GRUB_CMDLINE_LINUX=/s/"$/ fips=1"/' /etc/default/grub >> $LOG_FILE 2>&1
  echo "Verify the GRUB_CMDLINE_LINUX now has a fips=1 at the end of the line" >> $LOG_FILE
  cat /etc/default/grub >> $LOG_FILE 2>&1
  echo "" >> $LOG_FILE
  echo "Rebooting now" >> $LOG_FILE
  echo "" >> $LOG_FILE
  # shutdown -r now
  # Call shutdown in Ansible after this script completes
  echo "step 3 completed" >>$LOG_FILE.3done
  exit 0
  fi

if [ $1 -eq 4 ]
  then
  echo "Starting Pass 4" >> $LOG_FILE
  date >> $LOG_FILE
  echo "" >> $LOG_FILE
  echo "Confirm that FIPS is in enforcing mode after the reboot" >> $LOG_FILE
  echo "sysctl crypto.fips_enabled" >> $LOG_FILE
  sysctl crypto.fips_enabled >> $LOG_FILE 2>@1
  echo "" >> $LOG_FILE
  echo "Verifying key packages are correct version" >> $LOG_FILE
  rpm -qa fipscheck >> $LOG_FILE 2>&1
  rpm -qa hmaccalc >> $LOG_FILE 2>&1
  rpm -qa dracut-fips >> $LOG_FILE 2>&1
  rpm -qa kernel >> $LOG_FILE 2>&1
  rpm -qa openssl >> $LOG_FILE 2>&1
  rpm -qa openssh >> $LOG_FILE 2>&1
  rpm -qa libgcrypt >> $LOG_FILE 2>&1
  rpm -qa nss-softokn >> $LOG_FILE 2>&1
  rpm -qa gnutls >> $LOG_FILE 2>&1
  rpm -qa gmp >> $LOG_FILE 2>&1
  rpm -qa nettle >> $LOG_FILE 2>&1
  echo "" >> $LOG_FILE
  echo "Verification completed" >> $LOG_FILE
  date >> $LOG_FILE
  echo "step 4 completed" >>$LOG_FILE.4done
  fi
exit 0
