# Digital-Twin-RoomOcc

This project has been made on the 26th and 27th of January 2023 during the Digital Hackathon at the Technical University of Denmark. 

You can find the presentation slides on this [Awesome Google Slides](https://docs.google.com/presentation/d/1ij-4Z9UKbfmE00bBvATa5BiHUH9VU7xjIBrLUt6-E-M/edit?usp=sharing). 

## Pain

DTU Skylab welcomes thousands of student every year and is the home of a lot of student entrepreneurs. The free access and the free booking systems gather a lot of of meeting room bookings. However, all the bookings are not fulfilled whereas the rooms are still booked but unoccupied. 

## Solution 

Making a dashboard which availabilities of room by, on one hand, checking the outlook calendar[^1]	and on the other, predicting occupancy by analysing real-time data measurements empowered by [Climify](https://climify.com/).

[^1]: During the hackathon, it has been impossible to get access to the outlook calendar data for rooms at DTU, contacting the IT for further development

## Run the web app on your system 

First, download this [Github repository](https://github.com/bruadam/digitaltwin-hackathon-january23.git).

Then, you will need these libraries running on python 3.11.

```bash
pip install pandas numpy openpyxl streamlit
```

After, please run this command after being in the directory:

```bash
streamlit run .\app.py
```

or click on `__init.bat` available on the folder using Windows

## License

This project is protected given MIT License. 

But the ownership of the project and the data is shared by DTU Skylab, Climify and Bruno Adam. 

If you have any questions, please contact me by email on bruno.adam@pm.me