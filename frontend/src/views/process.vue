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
        请在左边选择框中选择好文件，点击按钮等待上传处理即可
      </span>
    </t-row>
    <t-row style="height: 3%" />
    <t-row style="height: 80%">
      <t-col
        :span="5"
        style="
          border: dashed;
          height: 100%;
          border-radius: 12px;
          border-color: steelblue;
        "
      >
        <t-button theme="primary" class="choice-button" size="large">
          <add-icon slot="icon" />
          请选择文件
        </t-button>
      </t-col>
      <t-col :span="2" style="height: 100%">
        <t-button class="process-button" theme="primary" shape="circle">
          <icon-font name="arrow-right" />
        </t-button>
      </t-col>
      <t-col
        :span="5"
        style="
          border: dashed;
          height: 100%;
          border-radius: 12px;
          border-color: steelblue;
        "
      >
        <span class="generation" style="font-family: cursive; font-size: 24px; font-weight: bold">
          生成区域
        </span>
      </t-col>
    </t-row>
  </div>
</template>

<script>
import { AddIcon, IconFont } from "tdesign-icons-vue";
export default {
  name: "process",
  components: { AddIcon, IconFont },
  data() {
    return {};
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
.choice-button {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
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
</style>