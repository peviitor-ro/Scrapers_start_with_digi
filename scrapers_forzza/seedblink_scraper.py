#
#
#
# New Scraper for SeedBlink Company
# Link ---> https://seedblink.com/careers
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid


def get_data_from_seedblink():
    """
    This script collect data from Simtel.
    """

    response = requests.get('https://seedblink.com/_next/data/KB-umt_VS-r-H9P1BQ3bO/en/careers.json').json()

    data = response['pageProps']['allJobs']

    # get data!
    lst_with_data = []
    for dt in data:
        link = dt['jobSlug']
        title = dt['data']['title']
        city = dt['data']['location']

        if city in ['Remote', 'Bucharest']:
            lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  'https://seedblink.com/en/careers/' + link,
                    "company": "seedblink",
                    "country": "Romania",
                    "city": city
                    })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'seedblink'
data_list = get_data_from_seedblink()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('seedblink',
                  'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTM3IiBoZWlnaHQ9IjMyIiB2aWV3Qm94PSIwIDAgMTM3IDMyIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8ZyBjbGlwLXBhdGg9InVybCgjY2xpcDBfNTU0Ml8xMjY3NzEpIj4KPHBhdGggZD0iTTExMy40NjcgMEwxMTMuMDkxIDAuNTUxMTk5TDEzMS42MDUgMTMuMjYxMUwxMDcuOTk4IDEuNTUyMjZMMTA3LjYyOSAyLjMwMTc3TDEzMC40ODEgMTMuNjM2N0wxMDMuNjUyIDUuMDAzNzVMMTAzLjM0NiA1Ljk1ODg1TDEyOS4zOTYgMTQuMzQxM0wxMDAuOTQ5IDkuODc4MTRMMTAwLjc2OSAxMS4wMzUyTDEyOC4xNTggMTUuMzMyNUwxMDAuMzQ5IDE1LjM0MDJWMTYuNjc4MUwxMjguMTMyIDE2LjY3MDdMMTAwLjc2OSAyMC45NjQ4TDEwMC45NDkgMjIuMTIxOUwxMjkuMzU0IDE3LjY3MTNMMTAzLjM0NiAyNi4wNDExTDEwMy42NTIgMjYuOTk2MkwxMzAuNDY5IDE4LjM2ODdMMTA3LjYyOSAyOS42OTgxTDEwNy45OTggMzAuNDQ3NkwxMzEuNTg5IDE4Ljc1MDFMMTEzLjA5MSAzMS40NDg3TDExMy40NjcgMzJMMTMyLjE1NyAxOS4xNjk4TDExOC41NzggMzAuOTc2NUwxMTguOTA3IDMxLjM1NTdMMTMxLjg4MyAyMC4wNzc0TDEyMy42MDUgMjguMzc4MUwxMjMuODQxIDI4LjYxNDdMMTM2LjQyMSAxNkwxMzYuMzAzIDE1Ljg4MTdMMTM2LjI5NSAxNS44NzM1TDEzNi4yODEgMTUuODU5NkwxMzYuMjYzIDE1Ljg0MThMMTM2LjI0MyAxNS44MjExTDEzNi4yMTcgMTUuNzk1OUwxMzYuMTg2IDE1Ljc2NEwxMzYuMTg1IDE1Ljc2MzRMMTM2LjE0MiAxNS43MjA0TDEzNi4wNzUgMTUuNjUzTDEzNS45NjYgMTUuNTQzNEwxMzUuODc4IDE1LjQ1NUwxMzUuNzYzIDE1LjM0MDJMMTM1Ljc1OCAxNS4zMzVMMTM1Ljc1MyAxNS4zMzA0TDEzNS43MyAxNS4zMDY3TDEzNS42NDkgMTUuMjI2MUwxMzUuNDU3IDE1LjAzMzJMMTMxLjQ1NiAxMS4wMjE0TDEyMy44NDEgMy4zODUxNkwxMjMuNjA1IDMuNjIxNzhMMTMxLjkwNyAxMS45NDY5TDExOC45MDcgMC42NDQxTDExOC41NzggMS4wMjMxN0wxMzIuMTUxIDEyLjgyNUwxMTMuNDY3IDBaIiBmaWxsPSIjMDMxNjM0Ii8+CjxwYXRoIGQ9Ik00LjAwMjEzIDEwLjg3NUM1LjY1MjkyIDEwLjg3NSA2Ljk0MTczIDExLjMwNiA3Ljg2ODk2IDEyLjE2NzRMNi44OTY0NyAxNC4wMjY4QzYuMDU5NzYgMTMuMzY5IDUuMTU1NTUgMTMuMDUyMiA0LjEzNzkgMTMuMDUyMkMzLjM5MTcxIDEzLjA1MjIgMi44NzE3MiAxMy40NTk3IDIuODcxNzIgMTMuOTM2MkMyLjg3MTcyIDE0LjU0ODcgMy43MzEwNiAxNC45MTA5IDQuNzkzNTggMTUuMTgzMkM2LjM1Mzg1IDE1LjUyMzQgOC4zODg5NiAxNi4yMjY4IDguMzY2MjMgMTguMzEyM0M4LjM2NjIzIDIwLjMwOCA2Ljc2MTE4IDIxLjU3NzcgNC4yNTA5NSAyMS41Nzc3QzMuMzY5MDggMjEuNTc3NyAyLjUwOTY1IDIxLjM5NjIgMS42NTA3OSAyMS4wMTA1QzAuODE0MDggMjAuNjI0OCAwLjI0ODQ0MSAyMC4yNCAwIDE5LjgzMTZMMS4yNjYwOSAxOC4xMzA5QzEuNTYwMjcgMTguNDcxMiAyLjAzNTAxIDE4Ljc2NjEgMi42OTA2OCAxOS4wMTU3QzMuMzQ2NDUgMTkuMjY0NCAzLjkxMTYxIDE5LjQwMDYgNC40MzE5OSAxOS40MDA2QzUuNTYyNCAxOS41MTM5IDYuMzUzODUgMTguMzEyMyA1LjIwMDgxIDE3LjcyMjVDMy43NzYzMiAxNi45NzQ2IDAuMjcxMDcgMTYuOTI5MyAwLjI3MTA3IDEzLjk4MTZDMC4yNzEwNyAxMi4wNTM5IDEuODMxMzQgMTAuODc1IDQuMDAyMTMgMTAuODc1WiIgZmlsbD0iIzAzMTYzNCIvPgo8cGF0aCBkPSJNMTkuMzc3MSAyMC4zMDhDMTguMzgyIDIxLjE0NjcgMTcuMDkzMSAyMS41Nzc2IDE1LjQ4NzYgMjEuNTc3NkMxMy44MzcyIDIxLjU3NzYgMTIuNTI1NCAyMS4wNzg1IDExLjUwODEgMjAuMTAzOEMxMC41MTMgMTkuMTI5IDEwLjAxNTYgMTcuODM1OSAxMC4wMTU2IDE2LjIyNjdDMTAuMDE1NiAxNC43MDc1IDEwLjUxMyAxMy40MzcgMTEuNDg1NSAxMi40MTY5QzEyLjQ1OCAxMS4zOTY4IDEzLjc2OTMgMTAuODc1IDE1LjM5NzEgMTAuODc1QzE2LjczMTYgMTAuODc1IDE3Ljg4NDYgMTEuMzI4NyAxOC44MTE4IDEyLjIxMjhDMTkuNzM4NyAxMy4wOTc1IDIwLjIxMzggMTQuMjMxMSAyMC4yMTM4IDE1LjYxNDJDMjAuMjEzOCAxNi4xODEzIDIwLjE2ODUgMTYuNjU3IDIwLjA1NTQgMTcuMDE5OUgxMi43MDY0QzEyLjkxMDEgMTguNTM5MiAxNC4xMzEgMTkuNDAwNCAxNS43NTkxIDE5LjQwMDRDMTYuOTEyMiAxOS40MDA0IDE3Ljg2MjEgMTkuMDgzNyAxOC42MzA5IDE4LjQ3MTJMMTkuMzc3MSAyMC4zMDhaTTEyLjYxNTkgMTUuMjczOEgxNy42MTMxQzE3LjYzNTggMTQuMDA0MSAxNi43MzE2IDEzLjA1MjIgMTUuMjg0NCAxMy4wNTIyQzEzLjgxNDYgMTMuMDUyMiAxMi45MTAxIDEzLjggMTIuNjE1OSAxNS4yNzM4WiIgZmlsbD0iIzAzMTYzNCIvPgo8cGF0aCBkPSJNMzAuOTc1NyAyMC4zMDhDMjkuOTgwNiAyMS4xNDY3IDI4LjY5MTkgMjEuNTc3NiAyNy4wODYyIDIxLjU3NzZDMjUuNDM1OCAyMS41Nzc2IDI0LjEyNCAyMS4wNzg1IDIzLjEwNjcgMjAuMTAzOEMyMi4xMTE2IDE5LjEyOSAyMS42MTQzIDE3LjgzNTkgMjEuNjE0MyAxNi4yMjY3QzIxLjYxNDMgMTQuNzA3NSAyMi4xMTE2IDEzLjQzNyAyMy4wODQxIDEyLjQxNjlDMjQuMDU2MSAxMS4zOTY4IDI1LjM2OCAxMC44NzUgMjYuOTk1OCAxMC44NzVDMjguMzMwMyAxMC44NzUgMjkuNDgzMiAxMS4zMjg3IDMwLjQxMDQgMTIuMjEyOEMzMS4zMzczIDEzLjA5NzUgMzEuODEyNCAxNC4yMzExIDMxLjgxMjQgMTUuNjE0MkMzMS44MTI0IDE2LjE4MTMgMzEuNzY3MyAxNi42NTcgMzEuNjU0MSAxNy4wMTk5SDI0LjMwNUMyNC41MDg2IDE4LjUzOTIgMjUuNzI5NSAxOS40MDA0IDI3LjM1NzggMTkuNDAwNEMyOC41MTA4IDE5LjQwMDQgMjkuNDYwNyAxOS4wODM3IDMwLjIyOTUgMTguNDcxMkwzMC45NzU3IDIwLjMwOFpNMjQuMjE0NSAxNS4yNzM4SDI5LjIxMThDMjkuMjM0NCAxNC4wMDQxIDI4LjMzMDMgMTMuMDUyMiAyNi44ODMxIDEzLjA1MjJDMjUuNDEzMyAxMy4wNTIyIDI0LjUwODYgMTMuOCAyNC4yMTQ1IDE1LjI3MzhaIiBmaWxsPSIjMDMxNjM0Ii8+CjxwYXRoIGQ9Ik00MC45OTE4IDIxLjMyODJWMjAuMjYyOEM0MC4yMDA0IDIxLjEwMTMgMzkuMjI4MyAyMS41MDk4IDM4LjA3NDggMjEuNTA5OEMzNi42Mjc2IDIxLjUwOTggMzUuNDc0NiAyMS4wMzMzIDM0LjU5MjYgMjAuMTA0QzMzLjcxMDYgMTkuMTUxMSAzMy4yODEyIDE3LjkwNDEgMzMuMjgxMiAxNi4zMzk1QzMzLjI4MTIgMTQuNzMwMyAzMy44MDEyIDEzLjQzNzIgMzQuODQxNCAxMi40MTdDMzUuODgxNCAxMS4zOTcgMzcuMjE1NSAxMC44NzUxIDM4Ljg2NjMgMTAuODc1MUMzOS43MjU2IDEwLjg3NTEgNDAuNDI2NSAxMS4wMzM5IDQwLjk5MTggMTEuMzc0M1Y1LjQ1NjA1SDQzLjU5MjRWMjEuMzI4Mkg0MC45OTE4Wk00MC45OTE4IDE4LjA0MDNWMTMuOTM2M0M0MC4zMzYxIDEzLjUyNzkgMzkuNjgwNCAxMy4zMjQ1IDM4Ljk3OTMgMTMuMzI0NUMzNy4zNTEyIDEzLjMyNDUgMzYuMDYyNCAxNC40MzU0IDM2LjA2MjQgMTYuMjQ4OEMzNi4wNjI0IDE3Ljk5NDkgMzcuMTcwMiAxOS4wODM5IDM4LjYxNzQgMTkuMDgzOUMzOS40OTkzIDE5LjA4MzkgNDAuMjkwOSAxOC43NDM1IDQwLjk5MTggMTguMDQwM1oiIGZpbGw9IiMwMzE2MzQiLz4KPHBhdGggZD0iTTQ2LjQ4NDQgNS40NTYwNUg0OS4wODQ2VjExLjc1OThDNDkuODMwOCAxMS4xNjk5IDUwLjczNTQgMTAuODc1IDUxLjc3NTcgMTAuODc1QzUzLjI2ODIgMTAuODc1IDU0LjQ0MzkgMTEuMzUxNSA1NS4zMDMzIDEyLjMyNjJDNTYuMTg1MiAxMy4yNzkgNTYuNjE0NiAxNC41MjYgNTYuNjE0NiAxNi4wNjhDNTYuNjE0NiAxNy43NDUzIDU2LjA5NDYgMTkuMDgzOCA1NS4wMzE3IDIwLjA4MTNDNTMuOTkxNyAyMS4wNzg2IDUyLjU4OTkgMjEuNTc3OCA1MC44MDMyIDIxLjU3NzhDNDkuMTk3OCAyMS41Nzc4IDQ3LjQ3OTQgMjEuMDc4NiA0Ni40ODQ0IDIwLjQ0NDJWNS40NTYwNVpNNDkuMDg0NiAxNC4yOTkyVjE4LjYzQzQ5LjYyNzUgMTguOTcwMyA1MC4yMzgyIDE5LjE1MSA1MC45MzkxIDE5LjE1MUM1Mi42MzUxIDE5LjE1MSA1My44MzMzIDE4LjA0MDIgNTMuODMzMyAxNi4yNDg3QzUzLjgzMzMgMTQuMzY3MyA1Mi43MDI1IDEzLjMyNDQgNTEuMTY1MyAxMy4zMjQ0QzUwLjMyODYgMTMuMzI0NCA0OS42NTAzIDEzLjY0MTIgNDkuMDg0NiAxNC4yOTkyWiIgZmlsbD0iIzAzMTYzNCIvPgo8cGF0aCBkPSJNNTguODc1IDUuNDU2MDVINjEuNDc1M1YxNy40NTExQzYxLjQ3NTMgMTguNTYyIDYxLjc2OTMgMTkuMTA2NSA2Mi4zNTcyIDE5LjEwNjVDNjIuNjk2NiAxOS4xMDY1IDYzLjAzNTQgMTguOTcwMyA2My40MjAxIDE4LjY5ODFMNjMuOTYyNyAyMC42OTNDNjMuMjYxNyAyMS4yNjAyIDYyLjM1NzIgMjEuNTU1MSA2MS4yNzIgMjEuNTU1MUM1OS42NjY1IDIxLjU1NTEgNTguODc1IDIwLjUzNSA1OC44NzUgMTguNTE2NlY1LjQ1NjA1WiIgZmlsbD0iIzAzMTYzNCIvPgo8cGF0aCBkPSJNNjcuMzc2MiA1LjkzMjYyQzY4LjE2NzYgNS45MzI2MiA2OC44NjgyIDYuNTQ0MzMgNjguODY4MiA3LjQ1MTgxQzY4Ljg2ODIgOC40NDkyOCA2OC4xNjc2IDkuMDgzNjkgNjcuMzc2MiA5LjA4MzY5QzY2LjQ0OSA5LjA4MzY5IDY1Ljc0OCA4LjQ0OTI4IDY1Ljc0OCA3LjQ1MTgxQzY1Ljc0OCA2LjU0NDMzIDY2LjQ3MTUgNS45MzI2MiA2Ny4zNzYyIDUuOTMyNjJaTTY2LjAxOTEgMTEuMTI0N0g2OC42MTk4VjIxLjMyODNINjYuMDE5MVYxMS4xMjQ3WiIgZmlsbD0iIzAzMTYzNCIvPgo8cGF0aCBkPSJNNzEuODk3NSAyMS4zMjg1VjExLjEyNDlINzQuNDk3N1YxMi4xNDVDNzUuMjQ0MyAxMS4zNTE4IDc2LjIxNjMgMTAuOTQzNCA3Ny40MTQ3IDEwLjk0MzRDODAuMTk1OSAxMC45NDM0IDgxLjU5NzggMTIuNDE3MyA4MS41OTc4IDE1LjM0MjNWMjEuMzI4NUg3OC45OTc2VjE1Ljc5NkM3OC45OTc2IDE0LjE4NjEgNzguMjI5MiAxMy4zOTIgNzYuNzE0MSAxMy4zOTJDNzUuODc3IDEzLjM5MiA3NS4xNTM4IDEzLjcwOTYgNzQuNDk3NyAxNC4zNjc1VjIxLjMyODVINzEuODk3NVoiIGZpbGw9IiMwMzE2MzQiLz4KPHBhdGggZD0iTTg2Ljg0MjUgNS40NTYwNUg4NC4yNDIyVjIxLjMyODJIODYuODQyNVY1LjQ1NjA1WiIgZmlsbD0iIzAzMTYzNCIvPgo8cGF0aCBkPSJNOTMuODA2OSAxMS4xMjVMODkuOTg1NiAxNS43OTYxTDk0LjI1OTQgMjEuMzI4Nkg5MC45MTI0TDg2Ljg4NzcgMTYuMDAwNEw5MC41Mjg3IDExLjEyNUg5My44MDY5WiIgZmlsbD0iIzAzMTYzNCIvPgo8L2c+CjxkZWZzPgo8Y2xpcFBhdGggaWQ9ImNsaXAwXzU1NDJfMTI2NzcxIj4KPHJlY3Qgd2lkdGg9IjEzNi40MjEiIGhlaWdodD0iMzIiIGZpbGw9IndoaXRlIi8+CjwvY2xpcFBhdGg+CjwvZGVmcz4KPC9zdmc+Cg=='
                  ))