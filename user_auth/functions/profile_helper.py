from user_auth.models import Profile


class ProfileHelper(object):
    def __init__(self, username):
        self.username = username

    def update_profile(self, nickname=None, img_url=None):
        if not nickname and not img_url:
            return
        try:
            row = Profile.objects.get(username=self.username)
            if nickname:
                row.nickname = nickname
            if img_url:
                row.img_url = img_url
            row.save()
        except Profile.DoesNotExist:
            Profile(
                username=self.username,
                nickname=nickname,
                img_url=img_url
            ).save()
        error_code = 0
        return error_code

    def get_profile(self):
        try:
            row = Profile.objects.get(username=self.username)
            profile_dict = dict(
                username=self.username,
                nickname=row.nickname,
                img_url=row.img_url
            )
            return profile_dict
        except Profile.DoesNotExist:
            return None

