#!/usr/bin/python3
import subprocess
import tempfile
import shutil
import zlib
import tarfile
import io

if __name__ == '__main__':
	tmpdir = tempfile.mkdtemp()
	print("Please connect a device with usb debugging enabled and this computer authorized. When asked, confirm the backup operation and DO NOT SET A PASSWORD")
	subprocess.run(["adb", "backup", "-f", "{}/backup".format(tmpdir), "net.daylio"])
	with open("{}/backup".format(tmpdir), "rb") as backupfile:
		backupfile.seek(24)
		data = zlib.decompress(backupfile.read())
		fp = io.BytesIO(data)
		tar = tarfile.open(fileobj=fp)
		db_fp = tar.extractfile("apps/net.daylio/db/entries.db")
		with open("entries.db", "wb") as outfile:
			outfile.write(db_fp.read())
	shutil.rmtree(tmpdir)
