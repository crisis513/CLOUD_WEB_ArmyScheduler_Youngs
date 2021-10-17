
<template>
  <v-app class="wrapper">
    <v-app class="main main-raised-sub">
      <div class="title-center">
        <h2>통계</h2>
      </div>
      <v-row
        justify="center"
      >
        <div class="left">
          <h3>총 근무시간</h3>
          <mdb-container>
            <mdb-bar-chart
              :data="barChartData"
              :options="barChartOptions"
              :width="400"
              :height="400"
            ></mdb-bar-chart>
          </mdb-container>
        </div>
        <div class="center">
        </div>
        <div class="right">
          <h3>기준별 근무시간</h3>
          <mdb-container>
            <mdb-bar-chart
              :data="barChartData2"
              :options="barChartOptions"
              :width="700"
              :height="400"
            ></mdb-bar-chart>
          </mdb-container>
        </div>
      </v-row>

      <v-row
        justify="center"
      >
        <div class="left">
          <v-simple-table
            fixed-header
            height="300px"
          >
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-center">
                    근무기준
                  </th>
                  <th class="text-center">
                    {{ barChartData.labels[0] }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr background-color="rgba(255, 206, 86, 0.5)">
                  <td>{{ barChartData.datasets[0].label }}</td>
                  <td>{{ barChartData.datasets[0].data[0] }}</td>
                </tr>
                <tr background-color="rgba(255, 206, 86, 1)">
                  <td>{{ barChartData.datasets[1].label }}</td>
                  <td>{{ barChartData.datasets[1].data[0] }}</td>
                </tr>
                <tr background-color="rgba(255, 99, 132, 0.5)">
                  <td>{{ barChartData.datasets[2].label }}</td>
                  <td>{{ barChartData.datasets[2].data[0] }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </div>
        <div class="center">
        </div>
        <div class="right">
          <v-simple-table
            fixed-header
            height="300px"
          >
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-center">
                    근무기준
                  </th>
                  <th class="text-center">
                    {{ barChartData2.labels[0] }}
                  </th>
                  <th class="text-center">
                    {{ barChartData2.labels[1] }}
                  </th>
                  <th class="text-center">
                    {{ barChartData2.labels[2] }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr background-color="rgba(255, 206, 86, 0.5)">
                  <td>{{ barChartData2.datasets[0].label }}</td>
                  <td>{{ barChartData2.datasets[0].data[0] }}</td>
                  <td>{{ barChartData2.datasets[0].data[1] }}</td>
                  <td>{{ barChartData2.datasets[0].data[2] }}</td>
                </tr>
                <tr background-color="rgba(255, 206, 86, 1)">
                  <td>{{ barChartData2.datasets[1].label }}</td>
                  <td>{{ barChartData2.datasets[1].data[0] }}</td>
                  <td>{{ barChartData2.datasets[1].data[1] }}</td>
                  <td>{{ barChartData2.datasets[1].data[2] }}</td>
                </tr>
                <tr background-color="rgba(255, 99, 132, 0.5)">
                  <td>{{ barChartData2.datasets[2].label }}</td>
                  <td>{{ barChartData2.datasets[2].data[0] }}</td>
                  <td>{{ barChartData2.datasets[2].data[1] }}</td>
                  <td>{{ barChartData2.datasets[2].data[2] }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </div>
        
      </v-row>
    </v-app>
  </v-app>
</template>

<script>
import { mdbBarChart, mdbContainer } from "mdbvue";
import axios from 'axios';
const BASE_URL = 'https://osamhack2021-cloud-web-armyscheduler-youngs-xr4vx9w4fvg7p-3000.githubpreview.dev'

export default {
  components: {
    mdbBarChart,
    mdbContainer
  },
  data: () => ({
    user_id: "u18",
    barChartData: {},
    barChartData2: {},
    barChartOptions: {
      responsive: false,
      maintainAspectRatio: false,
      scales: {
        xAxes: [
          {
            barPercentage: 0.8,
            gridLines: {
              display: true,
              color: "rgba(0, 0, 0, 0.1)"
            }
          }
        ],
        yAxes: [
          {
            gridLines: {
              display: true,
              color: "rgba(0, 0, 0, 0.1)"
            },
            ticks: {
              beginAtZero: true
            }
          }
        ]
      }
    },
  }),
  
  created () {
    const userssPath = BASE_URL + '/api/v1/users/'    
      axios.get(userssPath + this.user_id, this.user_id)
        .then((res) => {
          let eventsData = res.data["data"][0]
          this.barChartData = {
            labels: [
              "총 근무시간",
            ],
            datasets: [
              {
                label: "개인정비근무",
                data: [
                  eventsData.total_worked_time.free_worktime/60,
                ],
                backgroundColor: [
                  "rgba(255, 206, 86, 0.5)",
                ],
                borderColor: [
                  "rgba(255, 206, 86, 1)",
                ],
                borderWidth: 1
              },
              {
                label: "주간근무",
                data: [
                  eventsData.total_worked_time.day_worktime/60,
                ],
                backgroundColor: [
                  "rgba(255, 99, 132, 0.5)",
                ],
                borderColor: [
                  "rgba(255, 99, 132, 1)",
                ],
                borderWidth: 1
              },
              {
                label: "야간근무",
                data: [
                  eventsData.total_worked_time.night_worktime/60,
                ],
                backgroundColor: [
                  "rgba(54, 162, 235, 0.5)",
                ],
                borderColor: [
                  "rgba(54, 162, 235, 1)",
                ],
                borderWidth: 1
              },
            ]
          }
          this.barChartData2 = {
            labels: [
              "저번달 총 근무시간",
              "이번달 총 근무시간",
              "이번달 남은 근무시간",
            ],
            datasets: [
              {
                label: "개인정비근무",
                data: [
                  eventsData.prev_month_worked_time.free_worktime/60,
                  eventsData.this_month_worked_time.free_worktime/60,
                  eventsData.this_month_work_time_left.free_worktime/60,
                ],
                backgroundColor: [
                  "rgba(255, 206, 86, 0.5)",
                  "rgba(255, 206, 86, 0.5)",
                  "rgba(255, 206, 86, 0.5)",
                ],
                borderColor: [
                  "rgba(255, 206, 86, 1)",
                  "rgba(255, 206, 86, 1)",
                  "rgba(255, 206, 86, 1)",
                ],
                borderWidth: 1
              },
              {
                label: "주간근무",
                data: [
                  eventsData.prev_month_worked_time.day_worktime/60,
                  eventsData.this_month_worked_time.day_worktime/60,
                  eventsData.this_month_work_time_left.day_worktime/60,
                ],
                backgroundColor: [
                  "rgba(255, 99, 132, 0.5)",
                  "rgba(255, 99, 132, 0.5)",
                  "rgba(255, 99, 132, 0.5)",
                ],
                borderColor: [
                  "rgba(255, 99, 132, 1)",
                  "rgba(255, 99, 132, 1)",
                  "rgba(255, 99, 132, 1)",
                ],
                borderWidth: 1
              },
              {
                label: "야간근무",
                data: [
                  eventsData.prev_month_worked_time.night_worktime/60,
                  eventsData.this_month_worked_time.night_worktime/60,
                  eventsData.this_month_work_time_left.night_worktime/60,
                ],
                backgroundColor: [
                  "rgba(54, 162, 235, 0.5)",
                  "rgba(54, 162, 235, 0.5)",
                  "rgba(54, 162, 235, 0.5)",
                ],
                borderColor: [
                  "rgba(54, 162, 235, 1)",
                  "rgba(54, 162, 235, 1)",
                  "rgba(54, 162, 235, 1)",
                ],
                borderWidth: 1
              },
            ]
          }
        })
        .catch((error) => {
          console.error(error);
        });
  },

  methods: {

  },
}
</script>
