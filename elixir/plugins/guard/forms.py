from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, InputRequired
import random


class LoginForm(FlaskForm):
    email_placeholders = [
        # Star Trek
        "spock@enterprise.space",
        "picard@starfleet.federation",
        "kirk@boldlygo.net",
        "data@androiddreams.org",
        # Star Wars
        "vader@deathstar.galaxy",
        "yoda@theforce.net",
        "leia@rebellion.org",
        "hansolo@kesselrun12.com",
        # Firefly
        "mal@serenity.ship",
        "kaylee@shiny.engineering",
        "river@tam.siblings",
        # D&D
        "drizzt@underdark.dnd",
        "tiamat@fivedragons.net",
        "beholder@eyebeam.com",
        # Magic: The Gathering
        "jace@planeswalker.net",
        "chandra@pyromancy.com",
        "liliana@undeadminions.com",
        # Turtles (TMNT)
        "raph@ninjaturtles.sewers",
        "donnie@bo.staff",
        "mikey@pizza.lover",
        # Ghostbusters
        "venkman@whoyagonnacall.org",
        "slimer@ectoplasm.net",
        "staypuft@marshmallow.man",
        # He-Man
        "heman@eternia.power",
        "skeletor@snake.mountain",
        "she-ra@crystal.castle",
        # Sesame Street
        "elmo@sesamestreet.org",
        "cookiemonster@cookiecrave.com",
        "bigbird@yellowfeather.net",
        "oscar@grouchytown.bin",
        "bertandernie@roommate.fun",
        "grover@supermonster.blue",
        "count@ahahah.counting",
        # Muppets
        "kermit@rainbowconnection.com",
        "misspiggy@divastar.net",
        "fozzy@wockawocka.com",
        "gonzo@cannonstunt.show",
        "beaker@meepmeep.meep",
        "statlerandwaldorf@balconycritics.org",
        "rowlf@pianodog.tunes",
    ]

    password_placeholders = [
        "secretcode123",
        "tryGuessingThis",
        "noPeekin!",
        "very$secure",
        "dontTellAnyone",
        "lookAwayPlz",
        "password123",
        "letmein!",
        "trustno1",
        "abc123",
        "qwerty",
        "welcome",
        "iloveyou",
        "god",
    ]

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        # Randomly select from the lists
        self.email.render_kw = {"placeholder": random.choice(self.email_placeholders)}
        self.password.render_kw = {
            "placeholder": random.choice(self.password_placeholders)
        }

    # Fields
    email = StringField("email", render_kw={})

    password = PasswordField(
        "password", validators=[InputRequired(), DataRequired()], render_kw={}
    )
