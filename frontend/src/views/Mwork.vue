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
            max-width="300"
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
                  v-for="(item, i) in items"
                  :key="i"
                >
                  <v-list-item-content>
                    <v-list-item-title v-text="item.text"></v-list-item-title>
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
                <v-select
                  v-model="select"
                  :hint="`${select.state}, ${select.abbr}`"
                  :items="works"
                  item-text="state"
                  item-value="abbr"
                  label="근무지 선택"
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
                  근무설정
                </v-subheader>
              </v-col>
              <v-col cols="9">
                <table>
                  <tr v-for="(row, index) in rows" :key="index">
                    <td>
                      <v-text-field
                        slot="activator"
                        v-model="row.start"
                        label="시작시간 입력"
                        prepend-icon="access_time"
                        placeholder="00:00"
                        class="between-blank-10" ></v-text-field>
                    </td>
                    &nbsp;&nbsp;
                    <td>
                      <v-text-field
                        slot="activator"
                        v-model="row.end"
                        label="종료시간 입력"
                        prepend-icon="access_time"
                        placeholder="00:00"
                        class="between-blank-10" ></v-text-field>
                    </td>
                    <td>
                      <v-text-field
                        label="근무인원"
                        placeholder="0"
                      ></v-text-field>
                    </td>
                    <td><v-icon @click='deleteTableRow(index)'>delete</v-icon></td>
                  </tr>
                </table>
                <v-btn @click='addTableRow()' >근무 추가</v-btn>
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
                    <td>1. 이것은 테스트입니다.</td>
                    <td>
                      <v-radio-group
                        v-model="row"
                        row
                      >
                        <v-radio
                          label="Option 1"
                          value="radio-1"
                        ></v-radio>
                        <v-radio
                          label="Option 2"
                          value="radio-2"
                        ></v-radio>
                      </v-radio-group>
                    </td>
                  </tr>
                  <tr>
                    <td>2. 이것은 테스트</td>
                    <td>
                      <v-radio-group
                        v-model="row"
                        row
                      >
                        <v-radio
                          label="Option 1"
                          value="radio-1"
                        ></v-radio>
                        <v-radio
                          label="Option 2"
                          value="radio-2"
                        ></v-radio>
                      </v-radio-group>
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
                  근무주기
                </v-subheader>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  label="최소 근무주기 입력"
                  placeholder="2"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>

          <div class="title-center">
            <v-row
              align="center"
              justify="center"
            >
              <v-btn class="between-blank-50">초기화</v-btn>
              <v-btn class="between-blank-50" color="primary" @click="fetchDefaults">
                저장
              </v-btn>
            </v-row>
          </div>
          {{ work_cycle[0] }}
        </div>
      </div>
    </v-app>
  </v-app>
</template>

<script>
  import axios from 'axios';
  export default {
    data: () => ({
      selectedItem: 1,
      items: [
        { text: '위병소' },
        { text: 'CCTV' },
        { text: '순찰' },
      ],
      select: { state: '위병소', abbr: 'WB' },
      works: [
        { state: '위병소', abbr: 'WB' },
        { state: 'CCTV', abbr: 'CC' },
        { state: '순찰', abbr: 'SC' },
        { state: '창당직', abbr: 'CD' },
      ],
      work_cycle: [
        
      ],
      rows: [{
        start: "",
        end: ""
      }],
      counter: 1,
    }),
    methods:{
      fetchDefaults: function () {
        const path = 'https://osamhack2021-cloud-web-armyscheduler-youngs-xr4vx9w4fvg7p-3000.githubpreview.dev/api/v1/users/';
        axios.get(path)
          .then((res) => {
            this.work_cycle.push(res.data["data"][0]);
          })
          .catch((error) => {
            console.error(error);
          });
      },
      addTableRow: function () { 
        this.counter++;
        this.rows.push({start: "", end: ""});
      },
      deleteTableRow: function (idx) { 
        this.counter--;
        this.rows.splice(idx, 1);
      }
    }
  }
</script>