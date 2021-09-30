<template>
  <footer
    class="footer"
    :class="{ [`footer-${type}`]: type }"
    :data-background-color="backgroundColor"
  >
    <div class="container">
      <nav>
        <ul>
          <li>
            <a href="/#/landing">
              About Us
            </a>
          </li>
          <li>
            <a
              href="https://github.com/osamhack2021/CLOUD_WEB_ArmyScheduler_Youngs"
            >
              Git
            </a>
          </li>
          <li>
            <a href="https://www.creative-tim.com/license">
              Licenses
            </a>
          </li>
        </ul>
      </nav>
      <div class="copyright">
        &copy; {{ year }}, made with <md-icon>favorite</md-icon> by
        <a
          href="https://github.com/osamhack2021/CLOUD_WEB_ArmyScheduler_Youngs"
          target="_blank"
          >Army Scheduler</a
        >
        for a better military life.
      </div>
    </div>
  </footer>
</template>
<script>
export default {
  props: {
    backgroundColor: String,
    type: String
  },
  data() {
    return {
      year: new Date().getFullYear()
    };
  }
};
</script>
<style></style>
