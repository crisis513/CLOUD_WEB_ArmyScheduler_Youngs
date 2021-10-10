<template>
  <v-app class="wrapper">
    <v-app class="main main-raised-sub">
      <div class="title-center">
        <h2>부대 관리</h2>
      </div>
      <v-card>
        <v-row
        class="pa-4"
        justify="space-between"
        >
        <v-col cols="5">
          <v-card
            class="mx-auto"
            max-width="500"
          >
            <v-sheet class="pa-4 primary lighten-2">
              <v-text-field
                v-model="search"
                label="Search Company Directory"
                dark
                flat
                solo-inverted
                hide-details
                clearable
                clear-icon="mdi-close-circle-outline"
              ></v-text-field>
              <v-checkbox
                v-model="caseSensitive"
                dark
                hide-details
                label="Case sensitive search"
              ></v-checkbox>
            </v-sheet>
            <v-card-text>
              <v-treeview
                shaped
                hoverable
                activatable
                :items="items"
                :search="search"
                :filter="filter"
                :open.sync="open"
              >
                <template v-slot:prepend="{ item }">
                  <v-icon
                    v-if="item.userid"
                    v-text="`mdi-${item.userid === 'test_id' ? 'home-variant' : 'folder-network'}`"
                  ></v-icon>
                </template>
              </v-treeview>
            </v-card-text>
          </v-card>

          </v-col>

          <v-divider vertical></v-divider>

          <v-col
              class="d-flex text-center"
          >
            {{ items2 }}
          </v-col>
        </v-row>
      </v-card>
    </v-app>
  </v-app>
</template>

<script>
  import axios from 'axios';

  export default {
    data: () => ({
      items: [
        {
          name: 'Applications :',
          children: [
            { name: 'Calendar : app' },
            { name: 'Chrome : app' },
          ],
        },
        {
          name: 'Documents :',
          children: [
            {
              name: 'vuetify :',
              children: [
                {
                  name: 'src :',
                  children: [
                    { name: 'index : ts' },
                    { name: 'bootstrap : ts' },
                  ],
                },
              ],
            },
            {
              name: 'material2 :',
              children: [
                {
                  name: 'src :',
                  children: [
                    { name: 'v-btn : ts' },
                    { name: 'v-card : ts' },
                    { name: 'v-window : ts' },
                  ],
                },
              ],
            },
          ],
        },
      ],
      items2: null,
    }),

    created: function() {
      const path = 'https://osamhack2021-cloud-web-armyscheduler-youngs-xr4vx9w4fvg7p-3000.githubpreview.dev/api/v1/users/';
      axios.get(path)
        .then((res) => {
          let res_data = res.data["data"][0];
          this.items2 = res_data;
        })
        .catch((error) => {
          console.error(error);
        });
    },

    methods: {

    },
  }
</script>