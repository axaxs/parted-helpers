import subprocess
import shlex

def label_fs(fstype, part, label):
    ladic = {'ext2':'e2label %(part)s %(label)s',
             'ext3':'e2label %(part)s %(label)s',
             'ext4':'e2label %(part)s %(label)s',
             'fat':'mlabel -i %(part)s ::%(label)s',
             'fat16':'mlabel -i %(part)s ::%(label)s',
             'fat32':'mlabel -i %(part)s ::%(label)s',
             'ntfs':'ntfslabel %(part)s %(label)s',
             'jfs':'jfs_tune -L %(label)s %(part)s',
             'reiserfs':'reiserfstune -l %(label)s %(part)s',
             'xfs':'xfs_admin -l %(label)s %(part)s',
             'btrfs':'btrfs filesystem label %(part)s %(label)s'}
    fstype = fstype.lower()
    # OK, the below is a quick cheat.  vars() returns all variables
    # in a dictionary.  So 'part' and 'label' will be defined
    # and replaced in above dic
    try:
        y = subprocess.check_call(shlex.split(ladic[fstype] % vars()))
        ret = (0, y)
    except Exception as e:
        ret = (1, e)
        # check_call returns exit code.  0 should mean success
    return ret

def create_fs(part, fstype, label='', other_opts=None):
    #set some default options
    #-m 1 reserves 1% for root, because I think 5% is too much on
    #newer bigger drives.  
    #Also turn on dir_index for ext.  Not sure about other fs opts

    #The return value is tuple.  First arg is 0 for success, 1 for fail
    #Secong arg is either output from call if successful
    #or exception if failure

    opt_dic = {'ext2':'-m 1',
               'ext3':'-m 1 -O dir_index',
               'ext4':'-m 1 -O dir_index',
               'fat16':'',
               'fat32':'',
               'ntfs':'',
               'jfs':'',
               'reiserfs':'',
               'btrfs':'',
               'xfs':'',
               'swap':''} 
    fstype = fstype.lower()
    if not other_opts:
        other_opts = opt_dic[fstype]
    
    comdic = {'ext2':'mkfs.ext2 -c -L %(label)s %(other_opts)s %(part)s',
             'ext3':'mkfs.ext3 -c -L %(label)s %(other_opts)s %(part)s',
             'ext4':'mkfs.ext4 -c -L %(label)s %(other_opts)s %(part)s',
             'fat16':'mkfs.vfat -c -n %(label)s -F 16 %(other_opts) %(part)s',
             'fat32':'mkfs.vfat -c -n %(label)s -F 32 %(other_opts) %(part)s',
             'ntfs':'mkfs.ntfs -L %(label)s %(other_opts)s %(part)s',
             'jfs':'mkfs.jfs -c -L %(label)s %(other_opts)s %(part)s',
             'reiserfs':'mkfs.reiserfs -l %(label)s %(other_opts)s %(part)s',
             'xfs':'mkfs.xfs -L %(label)s %(other_opts)s %(part)s',
             'btrfs':'mkfs.btrfs -L %(label)s %(other_opts)s %(part)s',
             'swap':'mkswap %(part)s'}
    try:
        y = subprocess.check_output(shlex.split(comdic[fstype] % vars()))
        ret = (0, y)
    except Exception as e:
        ret = (1, e)
    return ret
