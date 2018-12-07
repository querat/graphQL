import  os
import  numpy
import  random
import  django
from    datetime        import datetime, timedelta
# from    matplotlib      import pyplot as mp

USERNAME = "test"
USERPASS = "test"

NB_SAMPLES          = 300
ISO_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "athome.settings"
)
django.setup()

from athome.api.models.Sample import Sample
from athome.api.models.User import User
from athome.api.models.Module import Module
from athome.api.models.Threshold import Threshold
from athome.api.models.Box import Box


def trunc_gauss(mu, sigma, bottom, top):
    a = random.gauss(mu, sigma)
    while (bottom <= a <= top) == False:
        a = random.gauss(mu, sigma)
        return a


def generateListOfGaussianDeltas(nbItems):
    def gaussian(x, mu, sig):
        return numpy.exp(-numpy.power(x - mu, 2.) / (2 * numpy.power(sig, 2.)))

    mu, sig = 0, 0.5

    nums = gaussian(numpy.linspace(-2, 2, nbItems // 2), mu, sig)

    # for samples slowly going Over then under the maximum threshold
    halfOfList = [(num * 1) for num in nums]
    # for samples slowly going Below then over the minimum threshold
    otherHalf = [(num * -1) for num in nums]
    result = halfOfList + otherHalf

    # enable this snippet if you wanna see the curves
    # mp.plot(result)
    # mp.show()

    return result * 2


def addFakeTimeLapseToSamples(listOfSamples):
    now = datetime.now()
    for x in range(NB_SAMPLES):
        timeElapsed = x * 30  # seconds
        fakeTimeStamp = (now + timedelta(seconds=timeElapsed))
        listOfSamples[x].date = fakeTimeStamp.strftime(ISO_DATETIME_FORMAT)



def makeTemperatureList(listOfDeltas):
    # 20 degrees Celsius + variations
    return [int(((delta * 15) + 20)) for delta in listOfDeltas]


if __name__ == "__main__":
    listOfSamples        = [Sample() for _ in range(NB_SAMPLES)]
    listOfRandomDeltas   = generateListOfGaussianDeltas(NB_SAMPLES)

    user = User.objects.filter(name=USERNAME).first()
    if user:
        for box in user.boxes.all():
            for module in box.modules.all():
                module.delete()
            box.delete()
        user.delete()

    import bcrypt
    user = User(
        name=USERNAME
        , password=bcrypt.hashpw(USERPASS.encode("utf8"), bcrypt.gensalt())
        , email='no@no.com'
    )
    user.save(force_insert=True)

    box = Box(
        user=user
        , authCode="authCodeHashHere"
    )
    box.save(force_insert=True)

    module = Module(
        mac="ee:ee:ee:ee:ee:ee"
        , name="test"
        , location="testRoom"
        , type="hygrometer"
        , vendor="AtHome"
        , authCode="authCodeHashHere"
        , box=box
    )
    module.save(force_insert=True)

    addFakeTimeLapseToSamples(listOfSamples)
    temperatures = makeTemperatureList(listOfRandomDeltas)
    for sample, temperature in zip(listOfSamples, temperatures):
        # °
        sample.payload = f'''{{ "unit_measure": "C", "measure":"{temperature}", "name":"Temperature" }}'''
        sample.module = module
        sample.save(force_insert=True)
