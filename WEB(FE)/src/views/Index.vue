<template>
  <div class="wrapper">
    <parallax class="section page-header header-filter" :style="headerStyle">
      <div class="container">
        <div class="md-layout">
          <div
            class="md-layout-item md-size-50 md-small-size-70 md-xsmall-size-100"
          >
            <h1 class="title">원클릭 근무표</h1>
            <h4>
              Army Scheduler는 근무표를 수정하느라 지친 간부와 불공정한 근무에 속앓이하는 용사들의 문제를 해결하고자 세상에 나오게 되었습니다.
            </h4>
            <br />
            <md-button
              href="https://www.youtube.com/channel/UCp-L48KrSB18I9yWnNoD69g"
              class="md-success md-lg"
              target="_blank"
              ><i class="fas fa-play"></i> Watch video</md-button
            >
          </div>
        </div>
      </div>
    </parallax>
    <div class="main main-raised">
      <div class="section">
        <div class="container">
          <div class="md-layout">
            <div
              class="md-layout-item md-size-66 md-xsmall-size-100 mx-auto text-center"
            >
              <h2 class="title text-center">Army Scheduler 소개</h2>
              <h5 class="description">
                대한민국의 거의 모든 군부대에서는 정해진 순번에 따라 미리 작성된 근무표를 통해 정해진 시간에 각자의 근무지에서 일을 합니다.
                하지만 용사들의 휴가와 부대 훈련 등으로 근무표가 변경될 때마다 순번은 꼬이기 마련이고 자칫하면 남들보다 과중하게 근무 투입되는 용사가 발생하는 경우가 많습니다.
                Army Scheduler을 통해 간편하고 공정한 근무를 생성하여 이러한 문제들을 해결할 수 있습니다.
              </h5>
            </div>
          </div>
          <div class="features text-center">
            <div class="md-layout">
              <div class="md-layout-item md-medium-size-33 md-small-size-100">
                <div class="info">
                  <div class="icon icon-info">
                    <md-icon>receipt_long</md-icon>
                  </div>
                  <h4 class="info-title">원클릭 근무표 작성</h4>
                  <p>
                    관리자 혹은 간부들이 클릭 한 번으로 원하는 기간만큼의 근무를 자동으로 생성해줍니다.
                    뿐만 아니라 같은 근무에 들어가는 인원들이 최대한 공평하도록 근무표를 제공합니다.
                  </p>
                </div>
              </div>
              <div class="md-layout-item md-medium-size-33 md-small-size-100">
                <div class="info">
                  <div class="icon icon-success">
                    <md-icon>analytics</md-icon>
                  </div>
                  <h4 class="info-title">개인 근무량 통계</h4>
                  <p>
                    근무자 혹은 용사들은 본인들이 근무하면서 개인정비시간, 취침시간에 얼마나 근무를 섰는지 통계를 통해 확인 가능합니다.
                    그리고 얼마나 공정하게 근무하고 있는지 전체 평균과 비교할 수 있습니다.
                  </p>
                </div>
              </div>
              <div class="md-layout-item md-medium-size-33 md-small-size-100">
                <div class="info">
                  <div class="icon icon-danger">
                    <md-icon>event_note</md-icon>
                  </div>
                  <h4 class="info-title">부대 일정 확인</h4>
                  <p>
                    관리자 혹은 간부들이 근무 외에 부대 일정을 생성하면 소속 용사들도 생성된 부대 일정을 확인할 수 있습니다.
                    나아가 용사 개인의 일정도 추가하여 자동으로 생성된 근무, 부대 일정 그리고 개인 일정을 한 화면에서 확인 가능합니다.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="section text-center">
        <div class="container">
          <h2 class="title text-center">개발인력</h2>
          <div class="team">
            <div class="md-layout">
              <div class="md-layout-item md-medium-size-33 md-small-size-100">
                <div class="team-player">
                  <md-card class="md-card-plain">
                    <div class="md-layout-item md-size-50 mx-auto">
                      <img
                        :src="teamImg1"
                        alt="Thumbnail Image"
                        class="img-raised rounded-circle img-fluid"
                      />
                    </div>
                    <h4 class="card-title">
                      이창림
                      <br />
                      <small class="card-description text-muted">
                        백엔드, 데이터베이스
                      </small>
                    </h4>

                    <md-card-content>
                      <p class="card-description">
                        You can write here details about one of your team
                        members. You can give more details about what they do.
                        Feel free to add some <a href="#">links</a> for people
                        to be able to follow them outside the site.
                      </p>
                    </md-card-content>

                    <md-card-actions class="text-center">
                      <md-button
                        href="javascript:void(0)"
                        class="md-just-icon md-simple"
                      >
                        <i class="fab fa-twitter"></i>
                      </md-button>
                      <md-button
                        href="javascript:void(0)"
                        class="md-just-icon md-simple"
                      >
                        <i class="fab fa-instagram"></i>
                      </md-button>
                      <md-button
                        href="javascript:void(0)"
                        class="md-just-icon md-simple"
                      >
                        <i class="fab fa-facebook-square"></i>
                      </md-button>
                    </md-card-actions>
                  </md-card>
                </div>
              </div>
              <div class="md-layout-item md-medium-size-33 md-small-size-100">
                <div class="team-player">
                  <md-card class="md-card-plain">
                    <div class="md-layout-item md-size-50 mx-auto">
                      <img
                        :src="teamImg2"
                        alt="Thumbnail Image"
                        class="img-raised rounded-circle img-fluid"
                      />
                    </div>
                    <h4 class="card-title">
                      손한기
                      <br />
                      <small class="card-description text-muted">
                        프론트엔드, 인프라
                      </small>
                    </h4>

                    <md-card-content>
                      <p class="card-description">
                        You can write here details about one of your team
                        members. You can give more details about what they do.
                        Feel free to add some <a href="#">links</a> for people
                        to be able to follow them outside the site.
                      </p>
                    </md-card-content>

                    <md-card-actions class="text-center">
                      <md-button
                        href="javascript:void(0)"
                        class="md-just-icon md-simple"
                      >
                        <i class="fab fa-twitter"></i>
                      </md-button>
                      <md-button
                        href="javascript:void(0)"
                        class="md-just-icon md-simple"
                      >
                        <i class="fab fa-linkedin"></i>
                      </md-button>
                    </md-card-actions>
                  </md-card>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  bodyClass: "index-page",
  props: {
    header: {
      type: String,
      default: require("@/assets/img/bg6.jpg")
    },
    teamImg1: {
      type: String,
      default: require("@/assets/img/young-man.png")
    },
    teamImg2: {
      type: String,
      default: require("@/assets/img/young-man2.png")
    },
  },
  data() {
    return {
      name: null,
      email: null,
      message: null
    };
  },
  computed: {
    headerStyle() {
      return {
        backgroundImage: `url(${this.header})`
      };
    }
  }
};
</script>

<style lang="scss" scoped>
.md-card-actions.text-center {
  display: flex;
  justify-content: center !important;
}
.contact-form {
  margin-top: 30px;
}

.md-has-textarea + .md-layout {
  margin-top: 15px;
}
</style>