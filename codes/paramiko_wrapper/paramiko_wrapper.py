import paramiko


class SFTPClient(paramiko.sftp_client.SFTPClient):
    def _transfer_with_callback(self, reader, writer, file_size, callback):
        size = 0
        while True:
            data = reader.read(3276800)
            writer.write(data)
            size += len(data)
            if len(data) == 0:
                break
            if callback is not None:
                callback(size, file_size)
        return size


paramiko.sftp_client.SFTPClient = SFTPClient

