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
        <h2>뭐넣지</h2>
      </div>


      <div class="space-50"></div>
      <md-divider md-inset></md-divider>
      <div class="space-50"></div>


    </div>
  </div>
</template>

<script>
import axios from 'axios';
const BASE_URL = 'https://osamhack2021-cloud-web-armyscheduler-youngs-xr4vx9w4fvg7p-3000.githubpreview.dev'

export default {
  components: {
  },
  name: "index",
  bodyClass: "index-page",
  props: {
    image: {
      type: String,
      default: require("@/assets/img/vue-mk-header.jpg")
    },
  },
  flag: true,
  data() {
    return {
      
    };
  },

  created () {
  },

  methods: {

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
