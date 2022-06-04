<template>
  <div class="history">
    <t-row style="height: 4%">
      <div>
        <img
          slot="history_img"
          class="history_img"
          src="../assets/history.png"
          alt="history_img"
          style="margin-left: 40px; width: 24px"
        />
      </div>
      <span
        style="
          font-family: cursive;
          font-size: 24px;
          font-weight: bold;
          margin-left: 10px;
        "
      >
        历史记录
      </span>
    </t-row>
    <t-row style="height: 5%" />
    <t-row style="height: 86%">

    </t-row>
  </div>
</template>

<script>
export default {
  name: "history",
  components: {},
  data() {
    return {
    };
  },
  methods: {
  },
};
</script>

<style>
.history {
  padding: 25px 75px;
  background: #ffffff;
  height: 100%;
}

</style>