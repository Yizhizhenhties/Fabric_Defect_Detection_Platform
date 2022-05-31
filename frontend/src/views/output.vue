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
          <img :src="row.srcimg" style="height: 40px" />
        </template>
        <template #path="{ row }">
          <img v-if="row.has_pro_img" :src="row.path" style="height: 40px" />
          <span v-else>{{ row.path }}</span>
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
      <t-row class="swiper-container">
        <swiper :options="swiperOption" class="swiper">
          <swiper-slide
            v-for="(item, index) in pro_imgList"
            :key="index"
            class="swiper-slide"
          >
            <img
              :src="item"
              style="
                background-position: 50%;
                background-size: cover;
                width: 100%;
              "
            />
          </swiper-slide>
          <div class="swiper-pagination" slot="pagination"></div>
        </swiper>
      </t-row>
      <t-divider />
      <t-row>
        <t-col :span="2">
          <h2 style="color: black; margin-left: 40px">检测总数：</h2>
        </t-col>
        <t-col :span="2">
          <h3 style="color: black; margin-left: 40px">{{ num_of_pro }}张</h3>
        </t-col>
        <t-col :span="2">
          <h2 style="color: black; margin-left: 40px">合格产品数量：</h2>
        </t-col>
        <t-col :span="2">
          <h3 style="color: black; margin-left: 40px">{{ num_of_true }}张</h3>
        </t-col>
        <t-col :span="2">
          <h2 style="color: black; margin-left: 40px">合格率：</h2>
        </t-col>
        <t-col :span="2">
          <h3 style="color: black; margin-left: 40px">{{ rate }}%</h3>
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
        :options="['纺织品识别错误', '缺陷部位识别错误', '缺陷部位定位不清晰']"
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
      pro_imgList: [],
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
        effect: "coverflow",
        grabCursor: true,
        centeredSlides: true,
        slidesPerView: "auto",
        coverflowEffect: {
          rotate: 50,
          stretch: 0,
          depth: 100,
          modifier: 1,
          slideShadows: true,
        },
        pagination: {
          el: ".swiper-pagination",
        },
      },
      num_of_pro: 0,
      num_of_true: 0,
      rate: 0,
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
          if (response.data.errcode === 0) {
            for (let i = 0; i < response.data.data.length; i++) {
              if (response.data.data[i].is_fabric) {
                this.pro_imgList.push(response.data.data[i].heat);
              }
              if (response.data.data[i].is_normal === "True") {
                this.num_of_true += 1;
              }
              this.data.push({
                id: i,
                srcimg: response.data.data[i].src_img,
                processdate: response.data.data[i].time,
                processoutput: response.data.data[i].is_normal,
                path: response.data.data[i].pro_img,
                report: "查看报告",
                has_pro_img: response.data.data[i].has_pro_img,
              });
            }
            // if (this.pro_imgList.length < 3) {
            //   this.swiperOption.slidesPerView = this.pro_imgList.length;
            //   console.log(this.swiperOption.slidesPerView)
            // }
            this.num_of_pro = this.pro_imgList.length;
            this.rate =
              (
                parseFloat(this.num_of_true) / parseFloat(this.num_of_pro)
              ).toFixed(2) * 100;
            this.loading = false;
          } else {
            this.$message.error("服务器连接失败");
          }
        })
        .catch((error) => {
          this.$message.error("服务器连接失败");
        });
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

<style lang="less">
.output {
  padding: 25px 75px;
  background: #ffffff;
  height: 100%;
}
.swiper-container {
  width: 100%;
  height: 200px;
}

.swiper {
  height: 100%;
  width: 100%;

  .swiper-slide {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 200px;
    height: 200px;
    text-align: center;
    font-weight: bold;
    background-position: center;
    background-size: cover;
  }

  .swiper-pagination {
    /deep/ .swiper-pagination-bullet.swiper-pagination-bullet-active {
      background-color: white;
    }
  }
}
</style>