
<template>
  <v-app class="wrapper">
    <v-app class="main main-raised-sub">
      <div class="title-center">
        <h2>근무 타임라인</h2>
      </div>
      <br><br>
      <div class="fill-height">
        <v-tabs v-model="type2">
          <v-tab @click="type2=0;changeTimeline()">6hours</v-tab>
          <v-tab @click="type2=1;changeTimeline()">12hours</v-tab>
          <v-tab @click="type2=2;changeTimeline()">1day</v-tab>
          <v-tab @click="type2=3;changeTimeline()">2day</v-tab>
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
            v-for="(event, index) in events2"
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
      </div>

      <md-divider md-inset></md-divider>

      <div class="title-center">
        <h2>일정</h2>
      </div>
      <v-row class="fill-height">
        <v-col>
          <v-container
            class="px-0"
            fluid
          >
            <v-switch
              v-model="switch1"
              label="근무표시"
            ></v-switch>
          </v-container>
          <v-sheet height="64">
            <v-toolbar
              flat
            >
              <v-btn
                outlined
                class="mr-4"
                color="grey darken-2"
                @click="setToday"
              >
                Today
              </v-btn>
              <v-btn
                fab
                text
                small
                color="grey darken-2"
                @click="prev"
              >
                <v-icon small>
                  mdi-chevron-left
                </v-icon>
              </v-btn>
              <v-btn
                fab
                text
                small
                color="grey darken-2"
                @click="next"
              >
                <v-icon small>
                  mdi-chevron-right
                </v-icon>
              </v-btn>
              <v-toolbar-title v-if="$refs.calendar">
                {{ $refs.calendar.title }}
              </v-toolbar-title>
              <v-spacer></v-spacer>
              <v-menu
                bottom
                right
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    outlined
                    color="grey darken-2"
                    v-bind="attrs"
                    v-on="on"
                  >
                    <span>{{ typeToLabel[type] }}</span>
                    <v-icon right>
                      mdi-menu-down
                    </v-icon>
                  </v-btn>
                </template>
                <v-list>
                  <v-list-item @click="type = 'day'">
                    <v-list-item-title>Day</v-list-item-title>
                  </v-list-item>
                  <v-list-item @click="type = 'week'">
                    <v-list-item-title>Week</v-list-item-title>
                  </v-list-item>
                  <v-list-item @click="type = 'month'">
                    <v-list-item-title>Month</v-list-item-title>
                  </v-list-item>
                  <v-list-item @click="type = '4day'">
                    <v-list-item-title>4 days</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-toolbar>
          </v-sheet>
          <v-sheet height="600">
            <v-calendar
              v-if="switch1"
              ref="calendar"
              v-model="focus"
              color="primary"
              :events="events"
              :event-color="getEventColor"
              :type="type"
              @click:event="showEvent"
              @click:more="viewDay"
              @click:date="viewDay"
            ></v-calendar>
            <v-calendar
              v-else
              ref="calendar"
              v-model="focus"
              color="primary"
              :events="oneEvent"
              :event-color="getEventColor"
              :type="type"
              @click:event="showEvent"
              @click:more="viewDay"
              @click:date="viewDay"
            ></v-calendar>
            
            <v-menu
              v-model="selectedOpen"
              :close-on-content-click="false"
              :activator="selectedElement"
              offset-x
            >
              <v-card
                color="grey lighten-4"
                min-width="700px"
                flat
              >
                <v-toolbar
                  :color="selectedEvent.event_color"
                  dark
                >
                  <v-toolbar-title>일정 확인</v-toolbar-title>
                  <v-spacer></v-spacer>
                  <v-btn icon @click="editCalendar()">
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn icon @click="result_alert = true">
                    <v-icon>mdi-minus-circle</v-icon>
                  </v-btn>
                  <md-dialog-confirm
                    :md-active.sync="result_alert"
                    md-title="일정 삭제"
                    md-content="해당 일정을 정말 삭제하시겠습니까?"
                    md-confirm-text="삭제"
                    md-cancel-text="취소"
                    @md-cancel="onCancel"
                    @md-confirm="deleteCalendar(selectedEvent.event_id)" />
                </v-toolbar>

                <v-container fluid>
                  <v-row align="center">
                    <v-col cols="3">
                      <v-subheader>
                        제목
                      </v-subheader>
                    </v-col>
                    <v-col cols="9">
                      <v-text-field
                        :value="selectedEvent.name"
                        v-model="selectedEvent.name"
                        :disabled="validated == 1"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
                
                <v-container fluid>
                  <v-row align="center">
                    <v-col cols="3">
                      <v-subheader>
                        일시
                      </v-subheader>
                    </v-col>
                    <v-col cols="9">
                      <table>
                      <tr>
                        <td>
                          <v-text-field
                            label="시작일자"
                            placeholder="2021-01-01"
                            prepend-icon="mdi-calendar"
                            :value="selectedEvent.str_start_date"
                            v-model="selectedEvent.str_start_date"
                            :disabled="validated == 1"
                          ></v-text-field>
                        </td>
                        <td>
                          <v-text-field
                            label="시작시간"
                            placeholder="00:00"
                            prepend-icon="access_time"
                            :value="selectedEvent.str_start_time"
                            v-model="selectedEvent.str_start_time"
                            :disabled="validated == 1"
                          ></v-text-field>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <v-text-field
                            label="종료일자"
                            placeholder="2021-01-01"
                            prepend-icon="mdi-calendar"
                            :value="selectedEvent.str_end_date"
                            v-model="selectedEvent.str_end_date"
                            :disabled="validated == 1"
                          ></v-text-field>
                        </td>
                        <td>
                          <v-text-field
                            label="종료시간"
                            placeholder="00:00"
                            prepend-icon="access_time"
                            :value="selectedEvent.str_end_time"
                            v-model="selectedEvent.str_end_time"
                            :disabled="validated == 1"
                          ></v-text-field>
                        </td>
                      </tr>
                      </table>
                    </v-col>
                  </v-row>
                </v-container>
                
                <v-container fluid>
                  <v-row align="center">
                    <v-col cols="3">
                      <v-subheader>
                        태그
                      </v-subheader>
                    </v-col>
                    <v-col cols="9">
                      <table>
                      <tr>
                        <td v-for="(tag, index) in selectedEvent.tags" :key="index" >
                          <v-chip
                            class="ma-2"
                            :color="tag.tag_color"
                            text-color="white"
                            v-model="selectedEvent.tags"
                            :value="selectedEvent.tags"
                            :close="showClose"
                            @click:close="selectedEvent.tags.splice(index, 1);"
                          >
                            {{ tag.tag_title }}
                          </v-chip>
                        </td>
                        <td>
                          <v-btn
                            class="mx-2"
                            fab
                            dark
                            small
                            color="indigo"
                            @click="addTagDialog = true"
                            v-if="isStatusOn"
                          >
                            <v-icon dark>
                              mdi-plus
                            </v-icon>
                          </v-btn>
                        </td>
                      </tr>
                      </table>
                    </v-col>
                  </v-row>
                </v-container>

                <table>
                <tr>
                  <td>
                    <v-card-actions>
                      <v-btn
                        text
                        color="secondary"
                        @click="selectedOpen = false"
                      >
                        종료
                      </v-btn>
                    </v-card-actions>
                  </td>
                  <td>
                    <v-card-actions>
                      <v-btn
                        text
                        color="primary"
                        @click="editCalendarComplete(selectedEvent)"
                        v-if="isStatusOn"
                      >
                        확인
                      </v-btn>
                    </v-card-actions>
                  </td>
                </tr>
                </table>
              </v-card>
            </v-menu>
          </v-sheet>
        </v-col>
      </v-row>

      <v-dialog
        v-model="addTagDialog"
        persistent
        max-width="500px"
      >
        <v-card>
          <v-card-title>
            <span class="text-h5">태그 설정</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col
                  cols="12"
                  sm="6"
                  md="4"
                >
                  <v-text-field
                    label="태그명*"
                    required
                    v-model="tag_title"
                  ></v-text-field>
                </v-col>
                <v-col
                  cols="12"
                  sm="6"
                  md="4"
                >
                  <v-text-field
                    label="태그색깔*"
                    required
                    hint="#RRGGBB"
                    v-model="tag_color"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-container>
            <small>*indicates required field</small>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="blue darken-1"
              text
              @click="addTagDialog = false"
            >
              종료
            </v-btn>
            <v-btn
              color="blue darken-1"
              text
              @click="addTagButton()"
            >
              생성
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      
      <div class="title-center">
        <v-row
          align="center"
          justify="center"
        >
          <v-dialog
            v-model="autoScheduleDialog"
            persistent
            max-width="500px"
            class="between-blank-10"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                max-width="150px"
                color="warning"
                @click="autoCreateWorkButtonClik()"
              >
                근무표 자동 생성
              </v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="text-h5">근무표 설정</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        label="시작일자*"
                        required
                        hint="2021-10-01"
                        v-model="event_start_date.date_string"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        label="종료일자*"
                        required
                        hint="2021-10-31"
                        v-model="event_end_date.date_string"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
                <small>*indicates required field</small>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="autoScheduleDialog = false"
                >
                  종료
                </v-btn>
                <v-btn
                  color="blue darken-1"
                  text
                  :disabled="loadingDialog"
                  :loading="loadingDialog"
                  @click="createWorkSchedule()"
                >
                  생성
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <v-dialog
            v-model="loadingDialog"
            hide-overlay
            persistent
            width="300"
          >
            <v-card
              color="primary"
              dark
            >
              <v-card-text>
                근무표 생성 중 ...
                <v-progress-linear
                  indeterminate
                  color="white"
                  class="mb-0"
                ></v-progress-linear>
              </v-card-text>
            </v-card>
          </v-dialog>

          <v-alert
            dense
            text
            type="success"
            v-if="success"
          >
            I'm a dense alert with the <strong>text</strong> prop and a <strong>type</strong> of success
          </v-alert>
          
          <v-dialog
            v-model="addScheduleDialog"
            persistent
            max-width="600px"
            class="between-blank-10"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                id="addCalendarBtn"
                v-bind="attrs"
                v-on="on"
                max-width="150px"
                color="primary"
              >
                일정 생성
              </v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="text-h5">일정 작성</span>
              </v-card-title>
              <v-card-text>

                <v-container fluid>
                  <v-row align="center">
                    <v-col cols="3">
                      <v-subheader>
                        제목
                      </v-subheader>
                    </v-col>
                    <v-col cols="6">
                      <v-text-field
                        v-model="addEvent.event_title"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
                
                <v-container fluid>
                  <v-row align="center">
                    <v-col cols="3">
                      <v-subheader>
                        제목색깔
                      </v-subheader>
                    </v-col>
                    <v-col cols="6">
                      <v-text-field
                        v-model="addEvent.event_color"
                        placeholder="#RRGGBB"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>

                <v-container fluid>
                  <v-row align="center">
                    <v-col cols="3">
                      <v-subheader>
                        일시
                      </v-subheader>
                    </v-col>
                    <v-col cols="9">
                      <table>
                      <tr>
                        <td>
                          <v-text-field
                            label="시작일자"
                            placeholder="2021-01-01"
                            prepend-icon="mdi-calendar"
                            v-model="addEvent.event_start_date.date_string"
                          ></v-text-field>
                        </td>
                        <td>
                          <v-text-field
                            label="시작시간"
                            placeholder="00:00"
                            prepend-icon="access_time"
                            v-model="addEvent.event_start_time"
                          ></v-text-field>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <v-text-field
                            label="종료일자"
                            placeholder="2021-01-01"
                            prepend-icon="mdi-calendar"
                            v-model="addEvent.event_end_date.date_string"
                          ></v-text-field>
                        </td>
                        <td>
                          <v-text-field
                            label="종료시간"
                            placeholder="00:00"
                            prepend-icon="access_time"
                            v-model="addEvent.event_end_time"
                          ></v-text-field>
                        </td>
                      </tr>               
                      </table>
                    </v-col>
                  </v-row>
                </v-container>
                
                <v-container fluid>
                  <v-row align="center">
                    <v-col cols="3">
                      <v-subheader>
                        태그
                      </v-subheader>
                    </v-col>
                    <v-col cols="9">
                      <table>
                        <tr v-for="(tag, index) in addEvent.tags" :key="index">
                          <td>
                            <v-text-field
                              slot="activator"
                              v-model="tag.tag_title"
                              label="태그명 입력"
                              class="between-blank-10" ></v-text-field>
                          </td>
                          &nbsp;&nbsp;
                          <td>
                            <v-text-field
                              slot="activator"
                              v-model="tag.tag_color"
                              label="태그색깔 입력"
                              placeholder="#RRGGBB"
                              class="between-blank-10" ></v-text-field>
                          </td>
                          <td><v-icon @click='deleteTableRow(index)'>delete</v-icon></td>
                        </tr>
                      </table>
                      <v-btn @click='addTableRow()' >태그 추가</v-btn>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  class="between-blank-50"
                  color="blue darken-1"
                  text
                  @click="addScheduleDialog = false"
                >
                  종료
                </v-btn>
                <v-btn
                  class="between-blank-50"
                  color="blue darken-1"
                  text
                  @click="addSchedule()"
                >
                  생성
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-row>
      </div>
    </v-app>
  </v-app>
</template>

<script>
  import { GGanttChart, GGanttRow } from "vue-ganttastic";
  import axios from 'axios';
  const BASE_URL = 'https://osamhack2021-cloud-web-armyscheduler-youngs-xr4vx9w4fvg7p-3000.githubpreview.dev'

  export default {
  components: {
    GGanttChart,
    GGanttRow,
  },
    data: () => ({
      getNowDate: "2021-10-14",
      getNowTime: "06:00",
      chartStart: "2021-10-14 17:00",
      chartEnd: "2021-10-15 05:00",
      highlightedHours: [],
      grid: true,
      type2: 0,
      users: [],

      focus: '',
      type: 'month',
      typeToLabel: {
        month: 'Month',
        week: 'Week',
        day: 'Day',
        '4day': '4 Days',
      },
      selectedEvent: {},
      selectedElement: null,
      selectedOpen: false,
      oneEvent: [],
      events: [],
      events2: [
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
      addEvent: {
        "event_id": null,
        "user_id": [],
        "event_title": null,
        "event_type": 1,
        "work_id": -1,
        "tags": [{
          "tag_title": null,
          "tag_color": null,
        }],
        "event_color": null,
        "event_start_date":{
          "date": 0,
          "date_string": null,
          "isHoliday": false
        },
        "event_start_time": null,
        "event_end_date": {
          "date": 0,
          "date_string": null,
          "isHoliday": false
        },
        "event_end_time": null
      },

      validated: 1,
      event_type: 1,
      isStatusOn: false,
      showClose: false,
      chipClose: true,
      addTagDialog: false,
      autoScheduleDialog: false,
      addScheduleDialog: false,
      loadingDialog: false,
      result_alert: false,
      event_start_date: {
        "date": 0,
        "date_string": null,
        "isHoliday": false
      },
      event_start_time: null,
      event_end_date: {
        "date": 0,
        "date_string": null,
        "isHoliday": false
      },
      event_end_time: null,
      counter: 1,
      switch1: false,
      scheduleResponse: [],
      success: false,
    }),

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
          let eventsData = res.data["data"][0]
          let event_list = []
          let one_event_list = []
          
          for (let i = 0; i < eventsData.length; i++) {
            if(eventsData[i].event_type == 0) {
              event_list.push({
                "event_id": eventsData[i].event_id, 
                "user_id": eventsData[i].user_id, 
                "name": eventsData[i].event_title, 
                "event_type": eventsData[i].event_type, 
                "work_id": eventsData[i].work_id, 
                "tags": eventsData[i].tags, 
                "event_color": eventsData[i].event_color, 
                "start": new Date(eventsData[i].event_start_date.date_string + "T" + eventsData[i].event_start_time), 
                "end": new Date(eventsData[i].event_end_date.date_string + "T" + eventsData[i].event_end_time),
                "str_start_date": eventsData[i].event_start_date.date_string,
                "str_end_date": eventsData[i].event_end_date.date_string,
                "str_start_time": eventsData[i].event_start_time,
                "str_end_time": eventsData[i].event_end_time,
                "timed": true 
              })
            } else if(eventsData[i].event_type == 1) {
              one_event_list.push({
                "event_id": eventsData[i].event_id, 
                "user_id": eventsData[i].user_id, 
                "name": eventsData[i].event_title, 
                "event_type": eventsData[i].event_type, 
                "work_id": eventsData[i].work_id, 
                "tags": eventsData[i].tags, 
                "event_color": eventsData[i].event_color, 
                "start": new Date(eventsData[i].event_start_date.date_string + "T" + eventsData[i].event_start_time), 
                "end": new Date(eventsData[i].event_end_date.date_string + "T" + eventsData[i].event_end_time),
                "str_start_date": eventsData[i].event_start_date.date_string,
                "str_end_date": eventsData[i].event_end_date.date_string,
                "str_start_time": eventsData[i].event_start_time,
                "str_end_time": eventsData[i].event_end_time,
                "timed": true 
              })
            }
          }
          this.oneEvent = one_event_list
          this.events = event_list

          for (let i = 0; i < eventsData.length; i++) {
            var start_datetime = eventsData[i].event_start_date.date_string + " " + eventsData[i].event_start_time
            var end_datetime = eventsData[i].event_end_date.date_string + " " + eventsData[i].event_end_time

            if(this.chartStart <= start_datetime || this.chartEnd >= end_datetime || (this.chartStart <= end_datetime && this.chartEnd >= start_datetime)) {
              for (let j = 0; j < this.events2.length; j++) {
                if(this.events2[j].event_title == eventsData[i].event_title) {
                  var user_list = []
                  
                  for(let k = 0; k < eventsData[i].user_id.length; k++) {
                    for(let l = 0; l < this.users.length; l++) {
                      if(eventsData[i].user_id[k] == this.users[l].user_id) {
                        user_list.push(this.users[l].name)
                        break
                      }
                    }
                  }
                  this.events2[j].bars.push({
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

    watch: {
      loadingDialog (val) {
        if (!val) return

        setTimeout(() => (this.loadingDialog = false), 5000)
      },
    },

    methods: {
      viewDay ({ date }) {
        this.focus = date
        this.type = 'day'
      },
      getEventColor (event) {
        return event.event_color
      },
      setToday () {
        this.focus = ''
      },
      prev () {
        this.$refs.calendar.prev()
      },
      next () {
        this.$refs.calendar.next()
      },
      showEvent ({ nativeEvent, event }) {
        const open = () => {
          this.selectedEvent = event
          this.selectedElement = nativeEvent.target
          requestAnimationFrame(() => requestAnimationFrame(() => this.selectedOpen = true))
        }

        if (this.selectedOpen) {
          this.selectedOpen = false
          requestAnimationFrame(() => requestAnimationFrame(() => open()))
        } else {
          open()
        }
        nativeEvent.stopPropagation()
      },

      addTagButton () {
        this.addTagDialog = false
      },
      createWorkSchedule () {
        this.loadingDialog = true
        const schedulePath = BASE_URL + '/api/v1/schedule/'
        
        var consider_date = new Date(Date.now() - (1000 * 60 * 60 * 24 * 30));  // 30일전
        var considerString = consider_date.getFullYear() + '-' 
            + ('0' + (consider_date.getMonth() + 1)).slice(-2)  
            + '-' + ('0' + consider_date.getDate()).slice(-2);

        axios.post(schedulePath, {
            "consider_from_date": considerString,
            "start_date": this.event_start_date.date_string,
            "end_date": this.event_end_date.date_string
          })
          .then((res) => {
            console.log(res)
            location.reload()
          })
          .catch((error) => {
            console.error(error);
          });

        this.addScheduleDialog = false
      },
      addSchedule () {
        this.addEvent.event_id = this.events.length + 1
        this.addEvent.user_id.push(this.user_id)
        this.addEvent.event_start_date.date = new Date(this.addEvent.event_start_date.date_string).getTime()
        this.addEvent.event_end_date.date = new Date(this.addEvent.event_end_date.date_string).getTime()
        const eventsPath = BASE_URL + '/api/v1/events/'

        axios.post(eventsPath, this.addEvent)
          .then((res) => {
            console.log(res.data)
          })
          .catch((error) => {
            console.error(error);
          });

        this.addScheduleDialog = false
        location.reload()
      },
      editCalendar () {
        if (this.validated == 0) {
          this.isStatusOn = false
          this.validated = 1
          this.showClose = false
        } else {
          this.isStatusOn = true
          this.validated = 0
          this.showClose = true
        }
      },
      editCalendarComplete (event) {
        const eventsPath = BASE_URL + '/api/v1/events/'
        axios.put(eventsPath + event.event_id, {
          "event_id": event.event_id,
          "user_id": event.user_id,
          "event_title": event.name,
          "event_type": event.event_type,
          "work_id": event.work_id,
          "tags": event.tags,
          "event_color": event.event_color,
          "event_start_date": {
            "date": Math.floor(new Date(event.str_start_date).getTime() / (1000 * 60 * 60 * 24)),
            "date_string": event.str_start_date,
            "isHoliday": false
          },
          "event_start_time": event.str_start_time,
          "event_end_date": {
            "date": Math.floor(new Date(event.str_end_date).getTime() / (1000 * 60 * 60 * 24)),
            "date_string": event.str_end_date,
            "isHoliday": false
          },
          "event_end_time": event.str_end_time
        })
        .then(res => {
          console.log(res)
        }).catch((ex) => {
          console.warn("Error: ", ex)
        })
        //location.reload()
      },
      deleteCalendar (event_id) {
        const eventsPath = BASE_URL + '/api/v1/events/'
        axios.delete(eventsPath + String(event_id), event_id)
          .then((res) => {
            console.log(res.data)
          })
          .catch((error) => {
            console.error(error);
          });
        location.reload()
      },
      oncancel () {
        this.result_alert = false
      },
      addTableRow: function () { 
        this.counter++;
        this.addEvent["tags"].push({tag_title: "", tag_color: ""});
      },
      deleteTableRow: function (idx) { 
        this.counter--;
        this.addEvent["tags"].splice(idx, 1);
      },
      changeTimeline () {
        var time = 0
        if (this.type2 == 0) {
          time = 6
        } else if (this.type2 == 1) {
          time = 12
        } else if (this.type2 == 2) {
          time = 24
        } else if (this.type2 == 3) {
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
      autoCreateWorkButtonClik () {
        var today = new Date();
        var year = today.getFullYear();
        var month = ('0' + (today.getMonth() + 1)).slice(-2);
        var day = ('0' + today.getDate()).slice(-2);

        var today30 = new Date(Date.now() + (1000 * 60 * 60 * 24 * 30));  // 30일후
        var year30 = today30.getFullYear();
        var month30 = ('0' + (today30.getMonth() + 1)).slice(-2);
        var day30 = ('0' + today30.getDate()).slice(-2);

        this.event_start_date.date_string = year + '-' + month  + '-' + day;
        this.event_end_date.date_string = year30 + '-' + month30  + '-' + day30;
      }
    },
  }
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

.v-text-field {
  width: 150px;
}
#addCalendarBtn {
  margin-left: 50px;
  margin-right: 50px;
}
</style>