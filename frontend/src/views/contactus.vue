<template>
  <div class="contactus">
    <t-row style="height: 4%">
      <div>
        <img
          slot="contactus_img"
          class="contactus_img"
          src="../assets/contactus.png"
          alt="contactus_img"
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
        联系我们
      </span>
    </t-row>
    <t-row style="height: 5%" />
  </div>
</template>

<script>
export default {
  name: "contactus",
  components: {},
  data() {
    return {};
  },
  methods: {},
};
</script>

<style>
.contactus {
  padding: 25px 75px;
  background: #ffffff;
  height: 100%;
}
</style>