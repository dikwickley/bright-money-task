from plaid.models import LogModel


def logger(api):
    log = LogModel.objects.create(api=api)
    log.save()
    print(f'{log.api} called at {log.date}')