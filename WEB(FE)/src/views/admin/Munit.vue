<template>
  <v-app class="wrapper">
    <v-app class="main main-raised-sub">
      <div class="title-center">
        <h2>부대 관리</h2>
      </div>
      <div class="parent">
        <div class="child1">
          <v-card
            class="mx-auto"
            max-width="450"
            elevation="1"
            tile
          >
            <v-sheet class="pa-4 primary lighten-2">
              <v-text-field
                v-model="search"
                label="Search"
                dark
                flat
                solo-inverted
                hide-details
                clearable
                clear-icon="mdi-close-circle-outline"
              ></v-text-field>
            </v-sheet>
            <v-card-text>
              <v-treeview 
                return-object 
                item-key="user_id" 
                hoverable 
                activatable 
                selected-color="blue"
                @update:active="updateForm" 
                :items="nowTreeData">
              </v-treeview>
              <template slot-scope="{ item }">
                <a @click="updateForm(item)">{{ item.name }}</a>
              </template>
            </v-card-text>
            <template>
              <div class="text-center">
                <v-pagination
                  v-model="page"
                  :length="page_length"
                  @input="pageClickEvent(page)"
                ></v-pagination>
              </div>
            </template>
          </v-card>
        </div>

        <v-divider vertical></v-divider>

        <div class="child2" v-if="name !== null">
          <v-container fluid>
            <v-row align="center">
              <v-col cols="3">
                <v-subheader>
                  이름
                </v-subheader>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  label="이름 입력"
                  placeholder="홍길동"
                  :value="name"
                  v-model="name"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
          
          <v-container fluid>
            <v-row align="center">
              <v-col cols="3">
                <v-subheader>
                  입대일
                </v-subheader>
              </v-col>
              <v-col cols="3">
                <v-text-field
                  slot="activator"
                  label="입대일 입력"
                  prepend-icon="mdi-calendar"
                  placeholder="2021-01-01"
                  :value="en_date"
                  v-model="en_date"
                  class="between-blank-10" ></v-text-field>
              </v-col>
              <v-col cols="3">
                <v-subheader>
                  전역예정일
                </v-subheader>
              </v-col>
              <v-col cols="3">
                <v-text-field
                  slot="activator"
                  label="전역예정일 입력"
                  prepend-icon="mdi-calendar"
                  placeholder="2022-01-01"
                  :value="de_date"
                  v-model="de_date"
                  class="between-blank-10" ></v-text-field>
              </v-col>
            </v-row>
          </v-container>

          <v-container fluid>
            <v-row align="center">
              <v-col cols="3">
                <v-subheader>
                   소속
                </v-subheader>
              </v-col>
              <v-col cols="6">
                <v-select
                  v-model="unit"
                  :items="unit"
                  label="소속 선택"
                  persistent-hint
                  return-object
                  single-line
                ></v-select>
              </v-col>
            </v-row>
          </v-container>

          <v-container fluid>
            <v-row align="center">
              <v-col cols="3">
                <v-subheader>
                  직책
                </v-subheader>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  label="직책 입력"
                  placeholder="소총수"
                  :value="position"
                  v-model="position"
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
              <v-col cols="5">
                <table>
                  <tr>
                    <td v-for="(work, index) in works" :key="index">
                      <md-checkbox 
                        v-model="work_list"
                        :value="work.work_id"
                      >
                        {{ work.work_name }}
                      </md-checkbox>
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
                  휴가 설정
                </v-subheader>
              </v-col>
              <v-col cols="7">
                <v-simple-table
                  fixed-header
                  height="300px"
                > 
                  <template v-slot:default>
                    <thead>
                      <tr>
                        <th class="text-left">
                          번호
                        </th>
                        <th class="text-left">
                          휴가출발일
                        </th>
                        <th class="text-left">
                          휴가복귀일
                        </th>
                        <th class="text-left">
                          휴가사유
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="(item, index) in vacation"
                        :key="index"
                      >
                        <td>{{ index+1 }}</td>
                        <td>{{ item.start_date }}</td>
                        <td>{{ item.end_date }}</td>
                        <td>{{ item.description }}</td>
                        <td><v-icon @click='deleteTableRow(index)'>delete</v-icon></td>
                      </tr>
                    </tbody>
                    
                    <v-dialog
                      v-model="vacation_dialog"
                      persistent
                      max-width="600px"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          dark
                          v-bind="attrs"
                          v-on="on"
                        >
                          휴가 추가
                        </v-btn>
                      </template>
                      <v-card>
                        <v-card-title>
                          <span class="text-h5">휴가 내용 작성</span>
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
                                  label="휴가출발일*"
                                  required
                                  hint="2021-03-01"
                                  v-model="start_date"
                                ></v-text-field>
                              </v-col>
                              <v-col
                                cols="12"
                                sm="6"
                                md="4"
                              >
                                <v-text-field
                                  label="휴가복귀일*"
                                  required
                                  hint="2021-03-05"
                                  v-model="end_date"
                                ></v-text-field>
                              </v-col>
                              <v-col
                                cols="12"
                                sm="6"
                                md="4"
                              >
                                <v-text-field
                                  label="휴가사유*"
                                  required
                                  hint="신병위로휴가"
                                  v-model="description"
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
                            @click="vacation_dialog = false"
                          >
                            종료
                          </v-btn>
                          <v-btn
                            color="blue darken-1"
                            text
                            @click="addTableRow()"
                          >
                            저장
                          </v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                  </template>
                </v-simple-table>
              </v-col>
            </v-row>
          </v-container>  

          <div class="title-center">
            <v-row
              align="center"
              justify="center"
            >
              <v-btn class="between-blank-50">삭제</v-btn>
              <v-btn class="between-blank-50" color="primary" @click="saveForm">
                저장
              </v-btn>
              <md-dialog-alert
                :md-active.sync="result_alert"
                md-title="정보 변경"
                md-content="입력하신 정보로 정상적으로 업데이트 되었습니다!" />
            </v-row>
          </div>          
        </div>
      </div>
    </v-app>
  </v-app>
</template>

<script>
  import axios from 'axios';
  const BASE_URL = 'https://osamhack2021-cloud-web-armyscheduler-youngs-xr4vx9w4fvg7p-3000.githubpreview.dev'

  export default {
    data: () => ({
      currentData: null,
      treeData: null,
      nowTreeData: [],

      name: null,
      user_id: null,
      password: null,
      email: null,
      is_admin: false,
      en_date: null,
      de_date: null,
      birth_date: null,
      now_class: null,
      unit: null,
      unit_company: null,
      unit_platoon: null,
      unit_squad: null,
      position: null,
      works: [],
      work_list: [],
      vacation: [],
      total_worked_time: {},
      this_month_worked_time: {},
      this_month_work_time_left: {},
      prev_month_worked_time: {},
      prev_day_worktime: 0,
      prev_night_worktime: 0,
      prev_free_worktime: 0,
      new_day_worktime: 0,
      new_night_worktime: 0,
      new_free_worktime: 0,
      fatigue: 0,

      start_date: null,
      end_date: null,
      description: null,

      result_alert: false,
      vacation_dialog: false,
      result: null,

      counter: 2,
      page: 1,
      page_length: 1,
    }),

    created () {
      const usersPath = BASE_URL + '/api/v1/users/';     
      axios.get(usersPath)
        .then((res) => {
          let usersData = res.data["data"][0];
          this.treeData = usersData;

          this.page_length = Math.floor(this.treeData.length / 15)
          for(let i = (this.page * 15) - 1; i < (this.page * 15) + 14; i++) {
            if(this.treeData[i].length < i) {
              break;
            }
            this.nowTreeData.push(this.treeData[i])
          }
        })
        .catch((error) => {
          console.error(error);
        });
      
      const worksPath = BASE_URL + '/api/v1/works/'
      axios.get(worksPath)
        .then((res) => {
          let worksData = res.data["data"][0];
          this.works = worksData;
        })
        .catch((error) => {
          console.error(error);
        });
    },

    methods: {
      updateForm: function (item) {
        if(item != null && item.length < 0) {
          console.error("error!!")
        }
        else {
          this.currentData = item

          this.name = item[0].name
          this.user_id = item[0].user_id
          this.password = item[0].password
          this.email = item[0].email
          this.is_admin = item[0].is_admin
          this.en_date = item[0].en_date
          this.de_date = item[0].de_date
          this.birth_date = item[0].birth_date
          this.now_class = item[0].now_class
          this.unit = item[0].unit_company 
              + " " + item[0].unit_platoon 
              + " " + item[0].unit_squad;
          this.unit_company = item[0].unit_company
          this.unit_platoon = item[0].unit_platoon
          this.unit_squad = item[0].unit_squad
          this.position = item[0].position
          this.work_list = item[0].work_list
          this.vacation = item[0].vacation
          this.total_worked_time = item[0].total_worked_time
          this.this_month_worked_time = item[0].this_month_worked_time
          this.this_month_work_time_left = item[0].this_month_work_time_left
          this.prev_month_worked_time = item[0].prev_month_worked_time
          this.prev_day_worktime = item[0].prev_day_worktime
          this.prev_night_worktime = item[0].prev_night_worktime
          this.prev_free_worktime = item[0].prev_free_worktime
          this.new_day_worktime = item[0].new_day_worktime
          this.new_night_worktime = item[0].new_night_worktime
          this.new_free_worktime = item[0].new_free_worktime
          this.fatigue = item[0].fatigue
        }
      },
      saveForm: function () {
        const usersPath = BASE_URL + '/api/v1/users/'
        axios.put(usersPath + this.user_id, {
            "name": this.name, 
            "user_id": this.user_id, 
            "password": this.password,
            "email": this.email,
            "is_admin": this.is_admin,
            "en_date": this.en_date,
            "birth_date": this.birth_date,
            "de_date": this.de_date, 
            "now_class": this.now_class,
            "unit_company": this.unit_company, 
            "unit_platoon": this.unit_platoon,
            "unit_squad": this.unit_squad, 
            "position": this.position,
            "work_list": this.work_list, 
            "vacation": this.vacation,
            "total_worked_time": this.total_worked_time,
            "this_month_worked_time": this.this_month_worked_time,
            "this_month_work_time_left": this.this_month_work_time_left,
            "prev_month_worked_time": this.prev_month_worked_time,
            "prev_day_worktime": this.prev_day_worktime,
            "prev_night_worktime": this.prev_night_worktime,
            "prev_free_worktime": this.prev_free_worktime,
            "new_day_worktime": this.new_day_worktime,
            "new_night_worktime": this.new_night_worktime,
            "new_free_worktime": this.new_free_worktime,
            "fatigue": this.fatigue,
          }
        ).then(res => {
          console.log(res)
          this.result_alert = true
        }).catch((ex) => {
          console.warn("Error: ", ex)
        })
        location.reload()
      },
      addTableRow: function () { 
        this.counter++
        this.vacation.push({start_date: this.start_date, end_date: this.end_date, description: this.description})
        this.start_date = null
        this.end_date = null
        this.description = null
        this.vacation_dialog = false
      },
      deleteTableRow: function (idx) { 
        this.counter--
        this.vacation.splice(idx, 1)
      },
      pageClickEvent (page) {
        this.nowTreeData = []
        for(let i = (page * 15) - 1; i < (page * 15) + 14; i++) {
          if(this.treeData[i].length < i) {
            break;
          }
          this.nowTreeData.push(this.treeData[i])
        }
      }
    },
  }
</script>
