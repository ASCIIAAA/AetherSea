import requests

url = "https://coastwatch.pfeg.noaa.gov/erddap/griddap/hycom_gom310D.nc?temperature%5B(2014-08-30T00:00:00Z):1:(2014-08-30T00:00:00Z)%5D%5B(0.0):1:(0)%5D%5B(25):1:(27)%5D%5B(-90):1:(-88)%5D,u%5B(2014-08-30T00:00:00Z):1:(2014-08-30T00:00:00Z)%5D%5B(0.0):1:(0)%5D%5B(25):1:(27)%5D%5B(-90):1:(-88)%5D,v%5B(2014-08-30T00:00:00Z):1:(2014-08-30T00:00:00Z)%5D%5B(0.0):1:(0)%5D%5B(25):1:(27)%5D%5B(-90):1:(-88)%5D"

response = requests.get(url)

with open("hycom_data.nc", "wb") as f:
    f.write(response.content)

print("Download complete!")