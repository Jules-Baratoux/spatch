# Spatch
Spatch is a [SSH][ssh] proxy server with ACL written in python using [Paramiko][paramiko].  
Authors: [Jules Baratoux][@jules] and [Pierre Jackman][@jack]

Spatch is a [SSH][ssh]v2 protocol deamon proxy with ACL. Users are allowed by Spatch to access to remote [SSH][ssh] servers without exposing real credentials.

```
USER 0 ◄──┐              ┌──► SSHD 1
USER 1 ◄──┴──► SPATCH ◄──┴──► SSHD 2
Users      Proxy server    End points
```

### Installation
1. As a privileged user, deploy and start `spatchd` on the proxy server
2. Deploy and start `sshd` on remote servers

### User creation
1. Register a remote server  
 `> spatch new server <host> <port>`
2. Create a spatch user  
 `> spatch new user <username> <user-rsa-public-key-filename>`
3. Grant access to a user on a remote server  
 `> grant <username> access to  <host> as <remote-username>`  
 From now on, a user given by `username` connecting to the spatch server with the specified *rsa-public-key* is able to connect to `host` using **ssh** as `remote-username`.

### User connection
1. Connect to spatch proxy server using any regular **ssh** client  
 `> ssh <username>@<spatch-host> -p <spatch-port>`
2. When prompted, select a `host` to connect to
3. You are now connected to the `host`

### Further help
Run `spatch` without specifying any command to get a full list of commands  
```
> spatch
usage:
    spatch <command>

commands:
    new server <hostname> <port>                      -- create a new server by name and port
    delete server <hostname>                          -- delete an existing server by name
    new user <username> <filename>                    -- create a new user by name and public key filename
    delete user <username>                            -- delete an existing user by name
    grant <username> access to <hostname> as <alias>  -- grant access to a user on an existing server as a remote user (alias)
    revoke <username> access from <hostname>          -- revoke access to a user from an existing server
    <username> has access to <hostname>               -- return whether a user has access to an existing server
    dump database to json                             -- dump the database in a json format
    export (users|servers) to <filename>              -- export a database section by name to a file given by filename
    import (users|servers) from <filename>            -- import a database section by name from a file given by filename
```

   [@jules]: <github.com/Jules-Baratoux>
   [@jack]: <github.com/Liek0s>
   [ssh]: <http://www.openssh.com>
   [paramiko]: <www.paramiko.org/>
