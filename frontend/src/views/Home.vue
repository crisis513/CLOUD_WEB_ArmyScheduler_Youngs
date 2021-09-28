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
      <g-gantt-chart :chart-start="myChartStart" :chart-end="myChartEnd">
        <g-gantt-row
          v-for="row in rows"
          :key="row.label"
          :label="row.label"
          :bars="row.bars"
          bar-start="myStart"
          bar-end="myEnd"
        />
      </g-gantt-chart>

      <div class="space-50"></div>
      <md-divider md-inset></md-divider>
      <div class="space-50"></div>

      <div class="title-center">
        <h2>스케줄 로그</h2>
      </div>
      <div class="md-layout">
        <div
          class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25"
        >
          <md-field>
            <md-input v-model="initial" placeholder="Regular"></md-input>
          </md-field>
        </div>
        <div
          class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25"
        >
          <md-field>
            <label>With Floating Label</label>
            <md-input v-model="floatingLabel" type="text"></md-input>
          </md-field>
        </div>
        <div
          class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25"
        >
          <md-field class="md-valid">
            <label>Success Input</label>
            <md-input v-model="success" type="text"></md-input>
            <md-icon>done</md-icon>
          </md-field>
        </div>
        <div
          class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25"
        >
          <md-field class="md-error">
            <label>Error Input</label>
            <md-input v-model="error" type="text"></md-input>
            <md-icon>clear</md-icon>
          </md-field>
        </div>
        <div
          class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25"
        >
          <md-field class="md-form-group">
            <md-icon>face</md-icon>
            <md-input
              v-model="withMIcon"
              placeholder="With Material Icons"
            ></md-input>
          </md-field>
        </div>
        <div
          class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25"
        >
          <md-field class="md-form-group">
            <i class="fas fa-users"></i>
            <md-input
              v-model="withFaIcon"
              placeholder="With Font Awesome Icons"
            ></md-input>
          </md-field>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { GGanttChart, GGanttRow } from "vue-ganttastic";

export default {
  components: {
    GGanttChart,
    GGanttRow
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
  methods: {},
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
