<template>
  <div class="aboutus">
    <t-row style="height: 4%">
      <div>
        <img
          slot="aboutus_img"
          class="aboutus_img"
          src="../assets/aboutus.png"
          alt="aboutus_img"
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
        关于我们
      </span>
    </t-row>
    <t-row style="height: 5%" />
  </div>
</template>

<script>
export default {
  name: "aboutus",
  components: {},
  data() {
    return {};
  },
  methods: {},
};
</script>

<style>
.aboutus {
  padding: 25px 75px;
  background: #ffffff;
  height: 100%;
}
</style>