#!/bin/bash
#take username and password
declare -A users;
login_user () {
    read -p "Enter user $1's username: " usr;
    read -sp "Enter user $1's password: " psd;
    echo ""
    declare -A tsvd_usr;
    declare -A tsvd_psd;
    index=0;
    while IFS=$'\t' read -r usr_i psd_i; do
        tsvd_usr[$index]="$usr_i";
        tsvd_psd[$index]="$psd_i";
        ((index++));
    done < users.tsv
    us_f=0;
    for ((i=0; i<index; i++)); do
        if [ "$usr" == "${tsvd_usr[$i]}" ]; then
            us_f=1;
            ps_f=${tsvd_psd[$i]};
            break;
        fi
    done
    if [ "$usr" == "" ] || [ "$psd" == "" ]; then
        echo "Username and password cannot be empty. Please try again."
        login_user $1
    fi
    if [ "$1" == "2" ] && [ ${users["user1"]} == "$usr" ]; then
        echo "User $1: $usr is already logged in. Please use a different username."
        login_user $1
    fi
    if [ $us_f -eq 0 ]; then
        read -p "Given username does not exist. Do you want to create new user? (y/n) " ch
        if [ $ch == "y" ]; then
            register_user $1
        else
            login_user $1
        fi
    else
        if [ "$(hash_pass "$psd")" == "$ps_f" ]; then
            echo "User $1: $usr has been successfully logged in."
            users["user$1"]=$usr;
            return 1
        else
            echo "Incorrect password. Please try again."
            login_user $1
        fi
    fi
}

register_user () {
    read -p "Enter new username: " usr_n;
    read -sp "Enter new password: " psd_n;
    echo ""
    uss=$(cut -f1 -d\t users.tsv);
    us_f=0;
    for i in $uss; do
        if [ "$usr_n" == "$i" ]; then
            us_f=1;
            break;
        fi
    done
    if [ $us_f -eq 0 ]; then
        echo -e "$usr_n\t$(hash_pass "$psd_n")" >> users.tsv
        echo "User $1: $usr_n has been successfully registered and logged in."
        users["user$1"]=$usr_n;
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
echo "Authentication of user 1: ${users["user1"]} and user 2: ${users["user2"]} is successful. You can now continue with the game hub."
python3 game.py ${users["user1"]} ${users["user2"]}