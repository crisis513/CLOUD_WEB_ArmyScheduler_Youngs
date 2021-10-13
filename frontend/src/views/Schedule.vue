
<template>
  <v-app class="wrapper">
    <v-app class="main main-raised-sub">
      <div class="title-center">
        <h2>스케줄</h2>
      </div>

      <v-row class="fill-height">
        <v-col>
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
            
            <v-menu
              v-model="selectedOpen"
              :close-on-content-click="false"
              :activator="selectedElement"
              offset-x
            >
              <v-card
                color="grey lighten-4"
                min-width="450px"
                flat
              >
                <v-toolbar
                  :color="selectedEvent.event_color"
                  dark
                >
                  <v-toolbar-title>일정 확인</v-toolbar-title>
                  <v-spacer></v-spacer>
                  <v-btn icon @click="calendarEdit">
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn icon>
                    <v-icon>mdi-minus-circle</v-icon>
                  </v-btn>
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
                        :disabled="validated == 1"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
                
                <v-container fluid>
                  <v-row align="center">
                    <v-col cols="3">
                      <v-subheader>
                        시간
                      </v-subheader>
                    </v-col>
                    <v-col cols="9">
                      <table>
                      <tr>
                        <td>
                          <v-text-field
                            label="시작시간"
                            placeholder="00:00"
                            prepend-icon="access_time"
                            :value="selectedEvent.str_start"
                            :disabled="validated == 1"
                          ></v-text-field>
                        </td>
                        <td>
                          <v-text-field
                            label="종료시간"
                            placeholder="00:00"
                            prepend-icon="access_time"
                            :value="selectedEvent.str_end"
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
                        <td v-for="(tag, index) in selectedEvent.tags" :key="index">
                          <v-chip
                            class="ma-2"
                            :color="tag.tag_color"
                            text-color="white"
                            v-if="chipClose"
                            v-model="tag.tag_title"
                            :close="showClose"
                            @click:close="chipClose = false"
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
                        @click="selectedOpen = false"
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
                    hint="red, green, blue ..."
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
      
      <v-dialog
        v-model="autoScheduleDialog"
        persistent
        max-width="500px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            v-bind="attrs"
            v-on="on"
            max-width="150px"
          >
            근무표 생성
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
                    label="시작일*"
                    required
                    hint="2021-10-01"
                    v-model="start_date"
                  ></v-text-field>
                </v-col>
                <v-col
                  cols="12"
                  sm="6"
                  md="4"
                >
                  <v-text-field
                    label="종료일*"
                    required
                    hint="2021-10-31"
                    v-model="end_date"
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
              @click="createWorkSchedule()"
            >
              생성
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      {{ events }}
    </v-app>
  </v-app>
</template>

<script>
  import axios from 'axios';
  const baseUrl = 'https://osamhack2021-cloud-web-armyscheduler-youngs-xr4vx9w4fvg7p-3000.githubpreview.dev'

  export default {
    data: () => ({
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
      events: [],
      
      validated: 1,
      isStatusOn: false,
      showClose: false,
      chipClose: true,
      addTagDialog: false,
      autoScheduleDialog: false,
      start_date: null,
      end_date: null,
      start_time: null,
      end_time: null,
    }),

    created () {
      const eventsPath = baseUrl + '/api/v1/events/'    
      axios.get(eventsPath)
        .then((res) => {
          let eventsData = res.data["data"][0]
          let event_list = []
          
          for (let i = 0; i < eventsData.length; i++) {
            event_list.push({
              "event_id": eventsData[i].event_id, 
              "userid": eventsData[i].userid, 
              "name": eventsData[i].event_title, 
              "event_type": eventsData[i].event_type, 
              "work_id": eventsData[i].work_id, 
              "tags": eventsData[i].tags, 
              "event_color": eventsData[i].event_color, 
              "start": new Date(eventsData[i].event_date + "T" + eventsData[i].start_time), 
              "end": new Date(eventsData[i].event_date + "T" + eventsData[i].end_time),
              "str_start": eventsData[i].start_time,
              "str_end": eventsData[i].end_time,
              "timed": true 
            })
            console.log(event_list)
          }
          this.events = event_list
        })
        .catch((error) => {
          console.error(error);
        });
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
        this.autoScheduleDialog = false
      },
      calendarEdit () {
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
      
    },
  }
</script>

<style scoped>
.v-text-field{
      width: 150px;
}
</style>