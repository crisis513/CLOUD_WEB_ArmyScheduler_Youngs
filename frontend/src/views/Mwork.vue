<template>
  <v-app class="wrapper">
    <v-app class="main main-raised-sub">
      <div class="title-center">
        <h2>근무 관리</h2>
      </div>
      <div class="parent">
        <div class="child1">
          <v-card
            class="mx-auto"
            max-width="450"
            elevation="1"
            tile
          >
            <v-list dense>
              <v-subheader>근무지</v-subheader>
              <v-list-item-group
                v-model="selectedItem"
                color="primary"
              >
                <v-list-item
                  v-for="(work, index) in works"
                  :key="index"
                  @click="updateForm(work)"
                >
                  <v-list-item-content>
                    <v-list-item-title 
                      v-text="work.work_name"
                    ></v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-card>
        </div>

        <v-divider vertical></v-divider>

        <div class="child2">
          <v-container fluid>
            <v-row align="center">
              <v-col cols="3">
                <v-subheader>
                  근무명
                </v-subheader>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  label="근무명 입력"
                  v-model="work.work_name"
                  :value="work.work_name"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>

          <v-container fluid>
            <v-row align="center">
              <v-col cols="3">
                <v-subheader>
                  근무설정
                </v-subheader>
              </v-col>
              <v-col cols="9">
                <table>
                  <tr v-for="(work_set, index) in work.work_setting" :key="index">
                    <td>
                      <v-text-field
                        slot="activator"
                        v-model="work_set.start_time"
                        :value="work_set.start_time"
                        label="시작시간 입력"
                        prepend-icon="access_time"
                        placeholder="00:00"
                        class="between-blank-10" ></v-text-field>
                    </td>
                    &nbsp;&nbsp;
                    <td>
                      <v-text-field
                        slot="activator"
                        v-model="work_set.end_time"
                        :value="work_set.end_time"
                        label="종료시간 입력"
                        prepend-icon="access_time"
                        placeholder="06:00"
                        class="between-blank-10" ></v-text-field>
                    </td>
                    <td>
                      <v-text-field
                        v-model="work_set.num_workers"
                        :value="work_set.num_workers"
                        label="근무인원"
                        placeholder="2"
                      ></v-text-field>
                    </td>
                    <td><v-icon @click='deleteTableRow(index)'>delete</v-icon></td>
                  </tr>
                </table>
                <v-btn @click='addTableRow()'>근무 추가</v-btn>
              </v-col>
            </v-row>
          </v-container>

          <v-container fluid>
            <v-row align="center">
              <v-col cols="3">
                <v-subheader>
                  근무옵션
                </v-subheader>
              </v-col>
              <v-col cols="9">
                <table>
                  <tr>
                    <td>1. 2일 연속 근무 여부</td>
                    <td>
                      <v-radio-group
                        v-model="work.work_option1"
                        :value="work.work_option1"
                        row
                      >
                        <v-radio
                          label="불가능"
                          value=0
                        ></v-radio>
                        <v-radio
                          label="가능"
                          value=1
                        ></v-radio>
                        <v-radio
                          label="무시"
                          value=2
                        ></v-radio>
                      </v-radio-group>
                    </td>
                  </tr>
                  <tr>
                    <td>2. 퐁당퐁당 근무 여부
                    <td>
                      <v-radio-group
                        v-model="work.work_option2"
                        :value="work.work_option2"
                        row
                      >
                        <v-radio
                          label="불가능"
                          value=0
                        ></v-radio>
                        <v-radio
                          label="가능"
                          value=1
                        ></v-radio>
                        <v-radio
                          label="무시"
                          value=2
                        ></v-radio>
                      </v-radio-group>
                    </td>
                  </tr>
                  <tr>
                    <td>3. 1일 2탕 여부</td>
                    <td>
                      <v-radio-group
                        v-model="work.work_option3"
                        :value="work.work_option3"
                        row
                      >
                        <v-radio
                          label="불가능"
                          value=0
                        ></v-radio>
                        <v-radio
                          label="가능"
                          value=1
                        ></v-radio>
                        <v-radio
                          label="무시"
                          value=2
                        ></v-radio>
                      </v-radio-group>
                    </td>
                  </tr>
                </table>
              </v-col>
            </v-row>
          </v-container>

          <div class="title-center">
            <v-row
              align="center"
              justify="center"
            >
              <v-btn class="between-blank-50">삭제</v-btn>
              <v-btn class="between-blank-50" color="primary">
                저장
              </v-btn>
            </v-row>
          </div>
        </div>
      </div>
      {{ works }}
      <br><br>
      {{ work }}
      <br><br>
      {{ counter }}
    </v-app>
  </v-app>
</template>

<script>
  import axios from 'axios';
  const baseUrl = 'https://osamhack2021-cloud-web-armyscheduler-youngs-xr4vx9w4fvg7p-3000.githubpreview.dev'

  export default {
    data: () => ({
      selectedItem: 0,
      works: [],
      work: {
        "work_id": 0,
        "work_name": null,
        "work_setting": [],
        "work_option1": 0,
        "work_option2": 0,
        "work_option3": 0,
      },
      counter: 0,
    }),

    created () {      
      const worksPath = baseUrl + '/api/v1/works/'
      axios.get(worksPath)
        .then((res) => {
          let worksData = res.data["data"][0];
          this.works = worksData;
        })
        .catch((error) => {
          console.error(error);
        });
    },

    methods:{
      updateForm: function (work) {
        var workForm = {
          "work_id": work.work_id,
          "work_name": work.work_name,
          "work_setting": work.work_setting,
          "work_option1": work.work_option1,
          "work_option2":work.work_option2,
          "work_option3": work.work_option3,  
        }
        this.work = workForm
        this.counter = 0
        var count = work.work_setting.length
        for(let i = 0; i < count; i++) {
          addTableRow(work.work_setting)
        }
      },
      saveForm: function () {
        
      },
      addTableRow: function (work_setting) { 
        this.counter++;
        this.work.work_setting.push({
          "start_time": work_setting.start_time, 
          "end_time": work_setting.end_time, 
          "num_workers": work_setting.num_workers
        });
      },
      deleteTableRow: function (idx) { 
        this.counter--;
        this.works.work_setting.splice(idx, 1);
      }
    }
  }
</script>