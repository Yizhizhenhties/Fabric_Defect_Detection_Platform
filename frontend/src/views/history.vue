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
    <t-row style="height: 91%" v-if="username">
      <t-table
        :data="data"
        :columns="columns"
        :rowKey="rowKey"
        :size="size"
        :loading="loading"
        :maxHeight="'100%'"
        style="height: 100%"
        bordered
      >
        <div slot="loading" class="t-table--loading-message">
          😊 请耐心等待结果 😊
        </div>
        <template #report="{ row }">
          <t-button
            @click="showReport(row.imgurls, row.length, row.pro_length)"
            :disabled="row.length === 0"
            >{{ row.report }}</t-button
          >
        </template>
      </t-table>
    </t-row>
    <t-row
      style="height: 91%; justify-content: center; align-content: center"
      v-else
    >
      <h3>😊 请登录后再使用历史记录功能 😊</h3>
    </t-row>
    <t-dialog
      :visible.sync="visible"
      :footer="false"
      :header="false"
      :width="'80%'"
      placement="center"
    >
      <t-loading :loading="loading_report">
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
      </t-loading>
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
  name: "history",
  components: {},
  data() {
    return {
      visible: false,
      visible1: false,
      pro_imgList: [],
      loading: true,
      loading_report: false,
      data: [],
      checked: [],
      columns: [
        {
          align: "center",
          width: "100",
          minWidth: "100",
          ellipsis: true,
          colKey: "uuid",
          title: "编号",
        },
        {
          align: "center",
          width: "100",
          minWidth: "100",
          ellipsis: true,
          colKey: "username",
          title: "用户名",
        },
        {
          align: "center",
          width: "100",
          minWidth: "100",
          ellipsis: true,
          colKey: "length",
          title: "检测有效张数",
        },
        {
          align: "center",
          width: "100",
          minWidth: "100",
          ellipsis: true,
          colKey: "createtime",
          title: "检测时间",
        },
        {
          align: "center",
          width: "100",
          minWidth: "100",
          ellipsis: true,
          colKey: "updatetime",
          title: "更新时间",
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
      rowKey: "uuid",
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
      username: sessionStorage.getItem("username"),
    };
  },
  methods: {
    getParams() {
      this.$http
        .post("/api/api/history/", {
          params: { username: this.username },
        })
        .then((response) => {
          if (response.data.errcode === 0) {
            for (let i = 0; i < response.data.data.length; i++) {
              this.data.push({
                uuid: response.data.data[i].uuid,
                username: response.data.data[i].username,
                length: response.data.data[i].length,
                pro_length: response.data.data[i].pro_length,
                imgurls: response.data.data[i].imgurls,
                createtime: response.data.data[i].createtime,
                updatetime: response.data.data[i].updatetime,
                report: "查看报告",
              });
            }
            this.loading = false;
          } else {
            this.$message.error("服务器连接失败");
          }
        })
        .catch((error) => {
          this.$message.error("服务器连接失败");
        });
    },
    showReport(imgurls, length, pro_length) {
      this.visible = true;
      this.loading_report = true;
      this.pro_imgList.length = 0;
      this.$http
        .post("/api/api/gethistoryimg/", {
          params: { imgurls: imgurls, length: length },
        })
        .then((response) => {
          if (response.data.errcode === 0) {
            for (var i = 0; i < length; i++) {
              this.pro_imgList.push(response.data.data[i].img);
              this.num_of_pro = length;
              this.num_of_true = pro_length;
              this.rate =
                (
                  parseFloat(this.num_of_true) / parseFloat(this.num_of_pro)
                ).toFixed(2) * 100;
            }
            this.loading_report = false;
          } else {
            this.$message.error("获取报告失败");
            this.loading_report = false;
          }
        })
        .catch((error) => {
          this.$message.error("服务器连接失败");
          this.loading_report = false;
        });
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
      let check_str = this.checked.join(";");
      this.$http
        .post("/api/api/addfeedback/", {
          params: { check: check_str, text: this.textdescription },
        })
        .then((response) => {
          if (response.data.errcode === 0) {
            this.checked = [];
            this.textdescription = "";
            this.confirmBtn = "提交反馈";
            this.visible1 = false;
            this.$message.success("提交反馈成功，我们会及时查看并解决");
          } else {
            this.confirmBtn = "提交反馈";
            this.$message.error("提交反馈失败");
          }
        })
        .catch((error) => {
          this.confirmBtn = "提交反馈";
          this.$message.error("服务器连接失败");
        });
    },
  },
  created() {
    if (sessionStorage.getItem("username")) {
      this.getParams();
    }
  },
};
</script>

<style lang="less">
.history {
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