Simplified Yurplan client used during the organisation of PyConFR

Usage:

```python
>>> from yurplan import YurplanClient
>>> yurplan = YurplanClient()
# authentification is performed at instanciation and needs the following environment variables to be set:
# YURPLAN_EVENT_ID
# YURPLAN_API_KEY
# YURPLAN_EMAIL
# YURPLAN_PASSWORD
>>> yurplan.attendants()
[Attendant(first_name=u'Balthazar', last_name=u'Rouberol', email=u'brouberol@imap.cc')]
```