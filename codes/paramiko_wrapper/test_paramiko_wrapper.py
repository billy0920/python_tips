from paramiko_wrapper import paramiko


if __name__ == "__main__":
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(
        hostname="root",
        port=22,
        username="root",
        password="Changeme_123")
    sftp = ssh.open_sftp()
    sftp.put("D:/test.zip", "test.zip")
