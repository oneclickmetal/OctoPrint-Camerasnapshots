from urllib import urlretrieve

def take_snapshot(snapshot_url, target_path):
    urlretrieve(snapshot_url, target_path)