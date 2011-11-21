# -*- coding: UTF-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        print "----------------------------------------------"
        print "-----    Welcome to the jukebox setup    -----"
        print "----------------------------------------------"
        print ""

        print "1. Administrator account"
        print "----------------------------------------------"
        print ""
        admin_user = raw_input("\tUsername: ")
        admin_email = raw_input("\tE-mail: ")
        print ""

        # get authentication methods
        authentication = self.setAuthentication()
        while not authentication:
            authentication = self.setAuthentication()

        self.setup(admin_user, admin_email, authentication)

    def setAuthentication(self):
        print "2. Please select your authentication methods"
        print "----------------------------------------------"
        print "Available providers: Facebook, Twitter, Github"
        print ""

        print "2.1 Facebook"
        print "\tFacebook authentication requires setup of a Facebook app on "\
            "http://developers.facebook.com/setup/"
        facebook = self.readAppData("Facebook")
        print ""

        print "2.2 Twitter"
        print "\tTwitter authentication requires setup of a Twitter app on "\
            "https://dev.twitter.com/apps/new"
        twitter = self.readAppData("Twitter")
        print ""

        print "2.3 Github"
        print "\tGithub authentication requires setup of a Github app on "\
            "https://github.com/account/applications/new"
        github = self.readAppData("Github")
        print ""

        if facebook is None and twitter is None and github is None:
            print "Are your kidding me? Why didn't you select a provider?"
            print "I won't let you go until you select at least one of them."
            print ""
            return False

        return {
            "facebook": facebook,
            "twitter": twitter,
            "github": github,
        }

    def readAppData(self, name):
        type = raw_input(
            "\tUse " + name + " for authentication? [y/n] "
        ).strip().lower()
        while type != "n" and type != "y":
            type = raw_input(
                "\tInvalid answer, please enter 'y' for yes or 'n' for no: "
            ).strip().lower()

        if type == "y":
            id = ""
            while id.strip() == "":
                id = raw_input("\t" + name + " app id: ")
                if id.strip() == "":
                    print "\t\tInvald app id"
            secret = ""
            while secret.strip() == "":
                secret = raw_input("\t" + name + " app secret: ")
                if secret.strip() == "":
                    print "\t\tInvald app id"

            return {
                "id": id,
                "secret": secret,
            }

        return None

    def setup(self, admin_user, admin_email, authentication):
        setup = open(settings.BASE_DIR + "/settings_local.example.py").read()

        setup = setup.replace("[admin_user]", admin_user)
        setup = setup.replace("[admin_email]", admin_email)

        auth_backends = []
        auth_backends_enabled = []

        if authentication["facebook"] is not None:
            auth_backends.append(
                "\"social_auth.backends.facebook.FacebookBackend\","
            )
            auth_backends_enabled.append("\"facebook\",")

        if authentication["twitter"] is not None:
            auth_backends.append(
                "\"social_auth.backends.twitter.TwitterBackend\","
            )
            auth_backends_enabled.append("\"twitter\",")

        if authentication["github"] is not None:
            auth_backends.append(
                "\"social_auth.backends.contrib.github.GithubBackend\","
            )
            auth_backends_enabled.append("\"github\",")

        setup = setup.replace(
            "[auth_backends]",
            "\n    ".join(auth_backends)
        )
        setup = setup.replace(
            "[auth_backends_enabled]",
            " ".join(auth_backends_enabled)
        )

        auth_data = ""
        for key, value in authentication.items():
            if value is None:
                continue

            if key == 'twitter':
                auth_data += "TWITTER_CONSUMER_KEY = \"" + \
                     value["id"] + "\"\n"
                auth_data += "TWITTER_CONSUMER_SECRET = \"" + \
                     value["secret"] + "\"\n"
            else:
                auth_data += key.upper() + "_APP_ID = \"" + \
                     value["id"] + "\"\n"
                auth_data += key.upper() + "_API_SECRET = \"" + \
                     value["secret"] + "\"\n"
            auth_data += "\n"

        setup = setup.replace("[auth_data]", auth_data)

        f = open(settings.BASE_DIR + "/settings_local.py", "w+")
        f.write(setup)
        f.close()

        print "Setup finished"
        print "----------------------------------------------"
