from datetime import datetime
import requests


class AppointmentChecker:

    def __init__(self, sucursals, month):
        self.sucursals = sucursals
        self.month = month
        self.sucursal_ids = list(sucursals.keys())
        self.url = 'https://bcrcita.bancobcr.com/citas/Home/Appointments_Found_Dates'
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': '<your_cookie>',
            'Origin': 'https://bcrcita.bancobcr.com',
            'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        self.payload = {
            'sucursalId': '',
            'servicioId': '23',
            'topicoId': '51'
        }

    def check(self):
        for sucursal_id in self.sucursal_ids:
            self.payload['sucursalId'] = str(sucursal_id)
            response = requests.post(self.url, headers=self.headers, data=self.payload)
            if response.status_code == 200:
                dates_list = response.json()
                for date_str in dates_list:
                    date = datetime.strptime(date_str, '%m/%d/%Y')
                    if date.month <= self.month:
                        yield f'{self.sucursals[sucursal_id]} ({date})'
                        break


if __name__ == '__main__':

    san_jose = {75: 'Barrio Amon', 169: 'Centro de Negocios Curridabat', 37: 'Desamparados', 141: 'Galería Escazú', 38: 'Guadalupe', 36: 'INS', 221: 'Los Colegios', 159: 'Multicentro Desamparados', 208: 'Multiplaza Curridabat', 46: 'Multiplaza Escazu', 214: 'Novacentro', 2: 'Oficinas Centrales', 43: 'Paseo Colon', 135: 'Paseo Estudiantes', 215: 'Plaza América', 4: 'Plaza Mayor', 176: 'Plaza Rhormorser', 35: 'Plazoleta', 132: 'Puriscal', 45: 'San Antonio Coronado', 131: 'San Francisco de Dos Rios', 7: 'San Isidro del General', 40: 'San Pedro Calle Real', 213: 'San Rafael Abajo Desamparados', 193: 'Tibas', 5: 'UCR'}
    cartago = {26: 'Cartago', 210: 'Pacayas', 65: 'Paseo Metrópoli', 34: 'San Rafael de Oreamuno', 220: 'Tejar del Guarco', 211: 'Terramall', 177: 'Tres Rios', 24: 'Turrialba'}
    heredia = {44: 'Centro Negocios Barreal', 17: 'Heredia Centro', 33: 'Heredia Cubujuqui', 170: 'Mall Oxigeno', 205: 'Paseo de las flores', 190: 'Puerto Viejo Sarapiquí', 59: 'San Antonio Belen', 127: 'Santo Domingo de Heredia'}

    sucursals = {**san_jose, **cartago, **heredia}
    month = 10  # October

    appt_checker = AppointmentChecker(sucursals, month)

    # check will yield the first element of the list, seems that is sorted asc
    for location in appt_checker.check():
        print(location)

