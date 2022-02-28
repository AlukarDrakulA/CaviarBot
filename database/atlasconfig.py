import requests
from requests.auth import HTTPDigestAuth
from ipify import get_ip

def atlasAccess():
    
    # TODO Полложить креды в config vars на herocu
    atlas_group_id = "621aaad69e52481334ef225b"
    atlas_api_key_public = "lyzbqlye"
    atlas_api_key_private = "949425b2-ca0f-4d2f-9509-c2a2fda54cc2"

    ip = get_ip()

    resp = requests.post(
        "https://cloud.mongodb.com/api/atlas/v1.0/groups/{atlas_group_id}/accessList".format(atlas_group_id=atlas_group_id),
        auth = HTTPDigestAuth(atlas_api_key_public, atlas_api_key_private),
        json=[{'ipAddress': ip, 'comment': 'From Herocu'}]  # the comment is optional
    )

    if resp.status_code in (200, 201):
        print("MongoDB Atlas accessList request successful", flush=True)
    else:
        print(
            "MongoDB Atlas accessList request problem: status code was {status_code}, content was {content}".format(
                status_code=resp.status_code, content=resp.content
            ),
            flush=True
        )

if __name__ == "__main__":
    atlasAccess()