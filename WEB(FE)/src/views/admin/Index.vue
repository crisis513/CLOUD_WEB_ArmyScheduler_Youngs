<template>
  <div class="wrapper">
    <parallax class="page-header header-filter" :style="headerStyle">
      <div class="md-layout">
        <div class="md-layout-item">
          <div class="image-wrapper">
            <div class="brand">
              <h1>Army Scheduler</h1>
              <h3>Youngs Team, Developers: Han-gi Son, Changrim Lee</h3>
            </div>
          </div>
        </div>
      </div>
    </parallax>

    <div class="main main-raised">
      <div class="space-50"></div>

      <div class="title-center">
        <h2>스케줄 타임라인</h2>
      </div>
      <br>

      <v-tabs v-model="type">
        <v-tab @click="type=0;changeTimeline()">6hours</v-tab>
        <v-tab @click="type=1;changeTimeline()">12hours</v-tab>
        <v-tab @click="type=2;changeTimeline()">1day</v-tab>
        <v-tab @click="type=3;changeTimeline()">2day</v-tab>
      </v-tabs>

      <g-gantt-chart 
        :chart-start="chartStart" 
        :chart-end="chartEnd"
        theme="creamy"
        row-height="35"
        :highlighted-hours="highlightedHours"
        :grid="grid"
      >
        <g-gantt-row
          v-for="(event, index) in events"
          :key="index"
          :label="event.event_title"
          :bars="event.bars"
          bar-start="start_time"
          bar-end="end_time"
        >
          <template #bar-label="{bar}">
            <h6>{{bar.label}}</h6>
          </template>
        </g-gantt-row>
      </g-gantt-chart>

      <div class="space-50"></div>
      <md-divider md-inset></md-divider>
      <div class="space-50"></div>

      <div class="title-center">
        <h2>차트 테스트</h2>
      </div>
      <br>
      <mdb-container>
        <mdb-bar-chart
          :data="barChartData"
          :options="barChartOptions"
          :width="1000"
          :height="300"
        ></mdb-bar-chart>
      </mdb-container>

      <div class="space-50"></div>
      <md-divider md-inset></md-divider>
      <div class="space-50"></div>

      <v-simple-table
        fixed-header
        height="300px"
      >
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">
                Name
              </th>
              <th class="text-left">
                Calories
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="d in desserts"
              :key="d.name"
            >
              <td>{{ d.name }}</td>
              <td>{{ d.calories }}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </div>
  </div>
</template>

<script>
import { GGanttChart, GGanttRow } from "vue-ganttastic";
import { mdbBarChart, mdbContainer } from "mdbvue";
import axios from 'axios';
const BASE_URL = 'https://osamhack2021-cloud-web-armyscheduler-youngs-xr4vx9w4fvg7p-3000.githubpreview.dev'

export default {
  components: {
    GGanttChart,
    GGanttRow,
    mdbBarChart,
    mdbContainer
  },
  name: "index",
  bodyClass: "index-page",
  props: {
    image: {
      type: String,
      default: require("@/assets/img/vue-mk-header2.jpg")
    },
  },
  data() {
    return {
      getNowDate: "2021-10-14",
      getNowTime: "06:00",
      chartStart: "2021-10-14 17:00",
      chartEnd: "2021-10-15 05:00",
      highlightedHours: [],
      grid: true,
      type: 0,
      users: [],
      events: [
        {
          "event_title": "당직",
          "bars": [],
        },
        {
          "event_title": "불침번",
          "bars": [],
        },
        {
          "event_title": "경계",
          "bars": [],
        },
      ],
      desserts: [
        {
          name: 'Frozen Yogurt',
          calories: 159,
        },
        {
          name: 'Ice cream sandwich',
          calories: 237,
        },
        {
          name: 'Eclair',
          calories: 262,
        },
      ],
    };
  },

  created () {
    var today = new Date();
    var today2 = new Date(Date.now() - (1000 * 60 * 60 * 2));
    var tomorrow = new Date(Date.now() + (1000 * 60 * 60 * 10));

    var year = today.getFullYear();
    var month = ('0' + (today.getMonth() + 1)).slice(-2);
    var day = ('0' + today.getDate()).slice(-2);

    var year2 = today2.getFullYear();
    var month2 = ('0' + (today2.getMonth() + 1)).slice(-2);
    var day2 = ('0' + today2.getDate()).slice(-2);

    var tomorrow_month = ('0' + (tomorrow.getMonth() + 1)).slice(-2);
    var tomorrow_day = ('0' + tomorrow.getDate()).slice(-2);

    var dateString = year + '-' + month  + '-' + day;
    var dateString2 = year2 + '-' + month2  + '-' + day2;
    var tomorrow_dateString = year + '-' + tomorrow_month  + '-' + tomorrow_day;

    var hours2 = ('0' + today2.getHours()).slice(-2);  
    var minutes2 = ('0' + today2.getMinutes()).slice(-2);
    var seconds2 = ('0' + today2.getSeconds()).slice(-2);

    var hours = ('0' + today.getHours()).slice(-2);  
    var minutes = ('0' + today.getMinutes()).slice(-2);
    var seconds = ('0' + today.getSeconds()).slice(-2);

    var hours6 = ('0' + tomorrow.getHours()).slice(-2);
    
    var minutes00 = "00"
    var seconds00 = "00"

    var timeString = hours + ':' + minutes  + ':' + seconds;
    var timeString00 = hours + ':' + minutes00  + ':' + seconds00;
    var timeString200 = hours2 + ':' + minutes00  + ':' + seconds00;
    var timeString600 = hours6 + ':' + minutes00  + ':' + seconds00;

    this.highlightedHours = [ Number(hours) ]

    this.chartStart = dateString2 + " " + timeString200
    this.chartEnd = tomorrow_dateString + " " + timeString600

    const usersPath = BASE_URL + '/api/v1/users/'    
    axios.get(usersPath)
      .then((res) => {
        var usersData = res.data["data"][0]
        this.users = usersData
        console.log(this.users)
      })
      .catch((error) => {
        console.error(error);
      });

    const eventsPath = BASE_URL + '/api/v1/events/'    
    axios.get(eventsPath)
      .then((res) => {
        var eventsData = res.data["data"][0]
        
        for (let i = 0; i < eventsData.length; i++) {
          var start_datetime = eventsData[i].event_start_date.date_string + " " + eventsData[i].event_start_time
          var end_datetime = eventsData[i].event_end_date.date_string + " " + eventsData[i].event_end_time

          if(this.chartStart <= start_datetime || this.chartEnd >= end_datetime || (this.chartStart <= end_datetime && this.chartEnd >= start_datetime)) {
            for (let j = 0; j < this.events.length; j++) {
              if(this.events[j].event_title == eventsData[i].event_title) {
                var user_list = []
                
                for(let k = 0; k < eventsData[i].user_id.length; k++) {
                  for(let l = 0; l < this.users.length; l++) {
                    if(eventsData[i].user_id[k] == this.users[l].user_id) {
                      user_list.push(this.users[l].name)
                      break
                    }
                  }
                }
                this.events[j].bars.push({
                  "event_id": eventsData[i].event_id, 
                  "user_id": eventsData[i].user_id,
                  "event_title": eventsData[i].event_title, 
                  "event_type": eventsData[i].event_type, 
                  "work_id": eventsData[i].work_id, 
                  "tags": eventsData[i].tags, 
                  "event_color": eventsData[i].event_color, 
                  "start_time": start_datetime,
                  "end_time": end_datetime,
                  "label": user_list.join(),
                  "ganttBarConfig": {
                    "color": "white", 
                    "backgroundColor": eventsData[i].event_color, 
                    "opacity": 0.9, 
                    "pushOnOverlap": false,
                    "immobile": true
                  }
                })
              }
            }
          }
        }
      })
      .catch((error) => {
        console.error(error);
      });
  },

  methods: {
    changeTimeline () {
      var time = 0
      if (this.type == 0) {
        time = 6
      } else if (this.type == 1) {
        time = 12
      } else if (this.type == 2) {
        time = 24
      } else if (this.type == 3) {
        time = 48
      }
      var today = new Date();
      var today2 = new Date(Date.now() - (1000 * 60 * 60 * 2));
      var tomorrow = new Date(Date.now() + (1000 * 60 * 60 * time));

      var year = today.getFullYear();

      var year2 = today2.getFullYear();
      var month2 = ('0' + (today2.getMonth() + 1)).slice(-2);
      var day2 = ('0' + today2.getDate()).slice(-2);

      var tomorrow_month = ('0' + (tomorrow.getMonth() + 1)).slice(-2);
      var tomorrow_day = ('0' + tomorrow.getDate()).slice(-2);

      var dateString2 = year2 + '-' + month2  + '-' + day2;
      var tomorrow_dateString = year + '-' + tomorrow_month  + '-' + tomorrow_day;

      var hours = ('0' + today.getHours()).slice(-2);  
      var hours2 = ('0' + today2.getHours()).slice(-2);  
      var hours6 = ('0' + tomorrow.getHours()).slice(-2);
      
      var minutes00 = "00"
      var seconds00 = "00"

      var timeString200 = hours2 + ':' + minutes00  + ':' + seconds00;
      var timeString600 = hours6 + ':' + minutes00  + ':' + seconds00;

      this.highlightedHours = [ Number(hours) ]

      this.chartStart = dateString2 + " " + timeString200
      this.chartEnd = tomorrow_dateString + " " + timeString600
    },
  },

  computed: {
    headerStyle() {
      return {
        backgroundImage: `url(${this.image})`
      };
    },
  },
  mounted() {},
  beforeDestroy() {}
};
</script>

<style lang="scss">
.section-download {
  .md-button + .md-button {
    margin-left: 5px;
  }
}

@media all and (min-width: 991px) {
  .btn-container {
    display: flex;
  }
}
</style>
