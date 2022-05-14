<template>
  <div class="helper">
    <t-row style="height: 4%">
      <div>
        <img
          slot="helper_img"
          class="helper_img"
          src="../assets/helper.png"
          alt="helper_img"
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
        帮助文档
      </span>
    </t-row>
    <t-row style="height: 5%" />
  </div>
</template>

<script>
export default {
  name: "helper",
  components: {},
  data() {
    return {};
  },
  methods: {},
};
</script>

<style>
.helper {
  padding: 25px 75px;
  background: #ffffff;
  height: 100%;
}
</style>