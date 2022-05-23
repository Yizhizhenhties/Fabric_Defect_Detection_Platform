<template>
  <div class="output">
    <t-row style="height: 4%">
      <div>
        <img
          slot="output_img"
          class="output_img"
          src="../assets/output.png"
          alt="output_img"
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
        结果查看
      </span>
    </t-row>
    <t-row style="height: 5%" />
    <t-row style="height: 91%">
      <t-table
        :data="data"
        :columns="columns"
        :rowKey="rowKey"
        :size="size"
        :loading="loading"
        :rowspanAndColspan="rowspanAndColspan"
        :maxHeight="'100%'"
        style="height: 100%"
        bordered
      >
        <div slot="loading" class="t-table--loading-message">
          😊 请耐心等待结果 😊
        </div>
        <template #srcimg="{ row }">
          <!-- <img :src="getObjectURL(row.srcimg)" style="height: 40px" /> -->
          <img :src="row.srcimg" style="height: 40px" />
        </template>
        <template #report="{ row }">
          <t-button @click="visible = true">{{ row.report }}</t-button>
        </template>
      </t-table>
    </t-row>
    <t-dialog
      :visible.sync="visible"
      :footer="false"
      :header="false"
      :width="'80%'"
      placement="center"
    >
      <t-row>
        <div>
          <img
            slot="reports_img"
            class="reports_img"
            src="../assets/reports.png"
            alt="reports_img"
            style="margin-left: 40px; width: 24px"
          />
        </div>
        <span
          style="
            font-family: cursive;
            font-size: 24px;
            margin-left: 10px;
            color: black;
          "
        >
          检测报告
        </span>
        <t-button
          theme="default"
          variant="text"
          style="margin-left: auto; color: cornflowerblue; margin-right: 20px"
          @click="visible1 = true"
          >对检测报告有疑问？点击这里反馈！</t-button
        >
      </t-row>
      <t-divider />
      <t-row>
        <h2 style="color: black; margin-left: 40px">检测效果：</h2>
      </t-row>
      <t-row style="place-content: center">
        <swiper :options="swiperOption" style="width: 80%; text-align: center">
          <swiper-slide v-for="(item, index) in imgList" :key="index" style="align-self: center">
            <img :src="getObjectURL(item.file)" style="width:200px" />
          </swiper-slide>
          <div class="swiper-pagination" slot="pagination"></div>
          <div class="swiper-button-prev" slot="button-prev"></div>
          <div class="swiper-button-next" slot="button-next"></div>
        </swiper>
      </t-row>
      <t-divider />
      <t-row>
        <t-col :span="2">
          <h2 style="color: black; margin-left: 40px">检测总数：</h2>
        </t-col>
        <t-col :span="2">
          <h3 style="color: black; margin-left: 40px">9张</h3>
        </t-col>
        <t-col :span="2">
          <h2 style="color: black; margin-left: 40px">合格产品数量：</h2>
        </t-col>
        <t-col :span="2">
          <h3 style="color: black; margin-left: 40px">9张</h3>
        </t-col>
        <t-col :span="2">
          <h2 style="color: black; margin-left: 40px">合格率：</h2>
        </t-col>
        <t-col :span="2">
          <h3 style="color: black; margin-left: 40px">100%</h3>
        </t-col>
      </t-row>
      <t-divider />
    </t-dialog>
    <t-dialog
      :visible.sync="visible1"
      theme="warning"
      header="提交反馈"
      :confirmBtn="confirmBtn"
      :onConfirm="onConfirm"
      :width="'60%'"
      placement="center"
    >
      <h3 style="color: black">常见问题：</h3>
      <t-checkbox-group
        v-model="checked"
        :options="['选项一', '选项二', '选项三']"
      ></t-checkbox-group>
      <t-divider />
      <h3 style="color: black">文字描述：</h3>
      <t-textarea v-model="textdescription" placeholder="请输入内容" />
    </t-dialog>
  </div>
</template>

<script>
export default {
  name: "Output",
  components: {},
  data() {
    return {
      visible: false,
      visible1: false,
      imgList: [],
      loading: true,
      data: [],
      checked: [],
      columns: [
        {
          align: "center",
          width: "100",
          minWidth: "100",
          ellipsis: true,
          colKey: "id",
          title: "编号",
        },
        {
          align: "center",
          width: "100",
          minWidth: "100",
          ellipsis: true,
          colKey: "srcimg",
          title: "原图",
        },
        {
          align: "center",
          width: "100",
          minWidth: "100",
          ellipsis: true,
          colKey: "processdate",
          title: "检测日期",
        },
        {
          align: "center",
          width: "100",
          minWidth: "100",
          ellipsis: true,
          colKey: "processoutput",
          title: "检测结果",
        },
        {
          align: "center",
          width: "100",
          minWidth: "100",
          ellipsis: true,
          colKey: "path",
          title: "缺陷部位",
        },
        {
          align: "center",
          width: "100",
          minWidth: "100",
          ellipsis: true,
          colKey: "report",
          title: "检测报告",
        },
      ],
      textdescription: "",
      confirmBtn: "提交反馈",
      rowKey: "id",
      size: "small",
      swiperOption: {
        slidesPerView: 3,
        pagination: {
          el: ".swiper-pagination",
          clickable: true,
        },
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
        autoplay: {
          delay: 2000,
        },
        loop: true,
      },
    };
  },
  methods: {
    getParams() {
      let data = this.$route.params.data;
      this.imgList = data;
      var imgfilelist = new FormData();
      this.imgList.forEach((value, index) => {
        imgfilelist.append("file", value.file);
      });
      this.$http
        .post("/api/api/process/", imgfilelist, {
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then((response) => {
          console.log(response);
          if (response.data.errcode === 0) {
            for (let i = 0; i < response.data.data.length; i++) {
              this.data.push({
                id: i,
                srcimg: response.data.data[i],
                processdate: "-",
                processoutput: "-",
                path: "-",
                report: "查看报告",
              });
            }
            if (this.imgList.length < 3) {
              this.swiperOption.slidesPerView = 1;
            }
            this.loading = false;
          } else {
            this.$message.error("服务器连接失败");
          }
        })
        .catch((error) => {
          this.$message.error("服务器连接失败");
        });
      // for (let i = 0; i < this.imgList.length; i++) {
      //   this.data.push({
      //     id: i,
      //     srcimg: this.imgList[i].file,
      //     processdate: "-",
      //     processoutput: "-",
      //     path: "-",
      //     report: "查看报告",
      //   });
      // }
      // if(this.imgList.length < 3){
      //     this.swiperOption.slidesPerView = 1
      // }
      // this.loading = false;
    },
    getObjectURL(file) {
      var url = null;
      if (window.createObjectURL != undefined) {
        // basic
        url = window.createObjectURL(file);
      } else if (window.URL != undefined) {
        // mozilla(firefox)
        url = window.URL.createObjectURL(file);
      } else if (window.webkitURL != undefined) {
        // webkit or chrome
        url = window.webkitURL.createObjectURL(file);
      }
      return url;
    },
    rowspanAndColspan({ col }) {
      if (col.colKey === "report") {
        return {
          rowspan: this.imgList.length,
        };
      }
    },
    onConfirm() {
      if (this.checked.length === 0 && this.textdescription === "") {
        this.$message.error("请选择常见反馈问题或填写文字反馈");
        return;
      }
      this.confirmBtn = {
        content: "提交中...",
        theme: "primary",
        loading: true,
      };
      //
      //请求
      //
      this.checked = [];
      this.textdescription = "";
      this.confirmBtn = "提交反馈";
      this.visible1 = false;
      this.$message.success("提交反馈成功，我们会及时查看并解决");
    },
  },
  created() {
    if (this.$route.params.data) {
      this.getParams();
    }
  },
};
</script>

<style>
.output {
  padding: 25px 75px;
  background: #ffffff;
  height: 100%;
}
@import "../../../node_modules/swiper/dist/css/swiper.css";
</style>