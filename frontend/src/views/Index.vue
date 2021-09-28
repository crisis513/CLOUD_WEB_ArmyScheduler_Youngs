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
      <div class="section section-basic">
        <div class="title-center">
            <h2>스케줄 타임라인</h2>
          </div>
          <g-gantt-chart
            :chart-start="myChartStart"
            :chart-end="myChartEnd"
          >
            <g-gantt-row
              v-for="row in rows"
              :key="row.label"
              :label="row.label"
              :bars="row.bars"
              bar-start="myStart"
              bar-end="myEnd"
            />
          </g-gantt-chart>
      </div>
    </div>
  </div>
</template>

<script>
import { GGanttChart, GGanttRow } from 'vue-ganttastic';

export default {
  components: {
    GGanttChart,
    GGanttRow,
  },
  name: "index",
  bodyClass: "index-page",
  props: {
    image: {
      type: String,
      default: require("@/assets/img/vue-mk-header.jpg")
    },
    signup: {
      type: String,
      default: require("@/assets/img/city.jpg")
    },
    landing: {
      type: String,
      default: require("@/assets/img/landing.jpg")
    },
    profile: {
      type: String,
      default: require("@/assets/img/profile.jpg")
    }
  },
  data() {
    return {
      firstname: null,
      email: null,
      password: null,
      leafShow: false,
      myChartStart: "2021-09-28 00:00",
      myChartEnd: "2021-09-30 06:00",
      rows: [
        {
          label: "위병소",
          bars: [
            {
              myStart: "2021-09-28 12:10",
              myEnd: "2021-09-28 16:35"
            }
          ]
        },
        {
          label: "CCTV",
          bars: [
            {
              myStart: "2021-09-28 01:00",
              myEnd: "2021-09-28 12:00"
            },
            {
              myStart: "2020-09-28 13:00",
              myEnd: "2020-09-28 22:00"
            }
          ]
        }
      ]
    };
  },
  methods: {
    
  },
  computed: {
    headerStyle() {
      return {
        backgroundImage: `url(${this.image})`
      };
    },
    signupImage() {
      return {
        backgroundImage: `url(${this.signup})`
      };
    }
  },
  mounted() {
  },
  beforeDestroy() {
  }
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
