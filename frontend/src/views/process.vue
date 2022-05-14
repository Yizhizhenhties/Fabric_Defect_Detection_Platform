<template>
  <div class="process">
    <t-row style="height: 4%">
      <div>
        <img
          slot="clothe"
          class="clothe"
          src="../assets/clothe.png"
          alt="clohte"
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
        纺织物缺陷检测
      </span>
    </t-row>
    <t-row style="height: 5%" />
    <t-row style="height: 8%">
      <span style="font-family: fangsong; font-size: 18px; margin-left: 30px">
        请点击左边选择框中的按钮选择图片(最多九张),点击传输按钮等待上传处理即可
      </span>
    </t-row>
    <t-row style="height: 3%" />
    <t-row style="height: 80%">
      <t-col
        :span="10"
        style="
          border: dashed;
          height: 100%;
          border-radius: 12px;
          border-color: steelblue;
        "
      >
      <up-img/>
      </t-col>
      <t-col :span="2" style="height: 100%">
        <t-button class="process-button" theme="primary" shape="circle">
          <icon-font name="arrow-right" />
        </t-button>
      </t-col>
    </t-row>
  </div>
</template>

<script>
import { AddIcon, IconFont } from "tdesign-icons-vue";
import UpImg from './upImg.vue'
export default {
  name: "process",
  components: { AddIcon, IconFont, UpImg },
  data() {
    return {
      files: [],
    };
  },
  methods: {},
};
</script>

<style>
.process {
  padding: 25px 75px;
  background: #ffffff;
  height: 100%;
}
.process-button {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
.generation {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
.tdesign-demo-upload-item {
  display: inline-block;
  margin-right: 80px;
}
.tdesign-demo-upload-item + .tdesign-demo-upload-item {
  margin-top: 80px;
}
</style>