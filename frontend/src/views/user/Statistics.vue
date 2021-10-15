
<template>
  <v-app class="wrapper">
    <v-app class="main main-raised-sub">
      <div class="title-center">
        <h2>통계</h2>
      </div>
      <br>
      <v-row class="fill-height">
        <v-col>
              
        </v-col>
      </v-row>
      
      <div class="title-center">
        <v-row
          align="center"
          justify="center"
        >

        </v-row>
      </div>
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
      addEvent: {
        "event_id": null,
        "user_id": -1,
        "event_title": null,
        "event_type": 1,
        "work_id": -1,
        "tags": [{
          "tag_title": null,
          "tag_color": null,
        }],
        "event_color": null,
        "event_start_date": null,
        "event_start_time": null,
        "event_end_date": null,
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
      event_start_date: null,
      event_start_time: null,
      event_end_date: null,
      event_end_time: null,
      counter: 1,
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
              "user_id": eventsData[i].user_id, 
              "name": eventsData[i].event_title, 
              "event_type": eventsData[i].event_type, 
              "work_id": eventsData[i].work_id, 
              "tags": eventsData[i].tags, 
              "event_color": eventsData[i].event_color, 
              "start": new Date(eventsData[i].event_start_date + "T" + eventsData[i].event_start_time), 
              "end": new Date(eventsData[i].event_end_date + "T" + eventsData[i].event_end_time),
              "str_start_date": eventsData[i].event_start_date,
              "str_end_date": eventsData[i].event_end_date,
              "str_start_time": eventsData[i].event_start_time,
              "str_end_time": eventsData[i].event_end_time,
              "timed": true 
            })
          }
          this.events = event_list
        })
        .catch((error) => {
          console.error(error);
        });
    },

    watch: {
      loadingDialog (val) {
        if (!val) return

        setTimeout(() => (this.loadingDialog = false), 3000)
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
        //this.autoScheduleDialog = false
      },
      addSchedule () {
        this.addEvent.event_id = this.events.length + 1
        const eventsPath = baseUrl + '/api/v1/events/'
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
        const eventsPath = baseUrl + '/api/v1/events/'
        axios.put(eventsPath + event.event_id, {
          "event_id": event.event_id,
          "user_id": event.user_id,
          "event_title": event.name,
          "event_type": event.event_type,
          "work_id": event.work_id,
          "tags": event.tags,
          "event_color": event.event_color,
          "event_start_date": event.str_start_date,
          "event_start_time": event.str_start_time,
          "event_end_date": event.str_end_date,
          "event_end_time": event.str_end_time
        })
        .then(res => {
          console.log(res)
        }).catch((ex) => {
          console.warn("Error: ", ex)
        })
        location.reload()
      },
      deleteCalendar (event_id) {
        const eventsPath = baseUrl + '/api/v1/events/'
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
      
    },
  }
</script>

<style scoped>
.v-text-field {
  width: 150px;
}
.v-btn {
  padding-right: 20px;
}
</style>