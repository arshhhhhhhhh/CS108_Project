#!/bin/bash
#take username and password

login_user () {
    read -p "Enter user $1's username: " usr;
    read -sp "Enter user $1's password: " psd;
    tsvd=$(cut -f1,2 -d\t users.tsv);
    stg=0;
    us_f=0;
    for i in tsvd; do
        if [ $stg -eq 0 ]; then
            if [ $usr == $i ]; then
                us_f=1;
            fi
            stg=1
        else
            if [ $us_f -eq 1 ]; then
                ps_f=i;
                break;
            fi
            stg=0
        fi
    done
    if [ $us_f -eq 0 ]; then
        read -p "Given username does not exist. Do you want to create new user? (y/n) " ch
        if [ $ch == "y" ]; then
            register_user $1
        else
            login_user $1
        fi
    else
        if [ $(hash_pass psd) == $ps_f ]; then
            return 1
        else
            login_user $1
        fi
    fi
}

register_user () {
    read -p "Enter new username: " usr_n;
    read -sp "Enter new password: " psd_n;
    uss=$(cut -f1 -d\t users.tsv);
    us_f=0;
    for i in uss; do
        if [ $usr_n == $i ]; then
            us_f=1;
            break;
        fi
    done
    if [ $us_f -eq 0 ]; then
        echo -e "$usr_n\t$(hash_pass psd_n)" >> users.tsv
    else
        echo "Given username already exists. Please use a different username."
        register_user $1
    fi
}

hash_pass () {
    #Hashing Password
    echo $1 | sha256sum
}

login_user 1
login_user 2