<template>
  <div class="wrapper">
    <div class="section page-header header-filter" :style="headerStyle">
      <div class="container">
        <div class="md-layout">
          <div
            class="md-layout-item md-size-33 md-small-size-66 md-xsmall-size-100 md-medium-size-40 mx-auto"
          >
            <login-card header-color="green">
              <h4 slot="title" class="card-title">Signup</h4>
              <md-field class="md-form-group" slot="inputs">
                <md-icon>face</md-icon>
                <label>이름</label>
                <md-input v-model="fullname"></md-input>
              </md-field>
              <md-field class="md-form-group" slot="inputs">
                <md-icon>email</md-icon>
                <label>이메일</label>
                <md-input v-model="email" type="email"></md-input>
              </md-field>
              <md-field class="md-form-group" slot="inputs">
                <md-icon>lock_outline</md-icon>
                <label>비밀번호</label>
                <md-input v-model="password" type="password"></md-input>
              </md-field>
              <md-button 
                slot="footer" 
                class="md-simple md-success md-lg"
                @click="$router.push('login')"
              >
                로그인
              </md-button>
              <md-button 
                slot="footer" 
                color="primary"
                class="md-simple md-primary md-lg"
                @click="requestSignup()"
              >
                회원가입
              </md-button>
            </login-card>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { LoginCard } from "@/components";
import axios from 'axios';
  const BASE_URL = 'https://osamhack2021-cloud-web-armyscheduler-youngs-xr4vx9w4fvg7p-3000.githubpreview.dev'

export default {
  components: {
    LoginCard
  },
  bodyClass: "login-page",
  data: () => ({
    fullname: null,
    email: null,
    password: null
  }),

  props: {
    header: {
      type: String,
      default: require("@/assets/img/signup_bg.jpg")
    }
  },
  computed: {
    headerStyle() {
      return {
        backgroundImage: `url(${this.header})`
      };
    }
  },

  methods: {
    requestSignup () {
      const signupPath = BASE_URL + '/jwt/admin'
      axios.post(signupPath, {
          "fullname": this.fullname, 
          "email": this.email, 
          "password": this.password
        })
      .then((res) => {
        console.log(res)
        if(res.status == 200) {
            this.$router.push('login')
          }
      })
      .catch((error) => {
        console.error(error);
      });
    }
  }
};
</script>