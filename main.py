import requests

message = requests.get("https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php?line=TML&sta=SIH")

print(message.text)