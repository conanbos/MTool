<template>
    <el-container direction="vertical">
        <el-dialog
                @opened='openPreviewDialog'
                @close="closePreviewDialog"
                title="PreView"
                :visible.sync="previewDialog"
                width="60%"
        >
            <el-container>
                <el-main class="seconds">
                    <div class="seconds_v" id="fuse"></div>
                </el-main>
            </el-container>
            <div ref="attr3"></div>
        </el-dialog>

        <el-container>
            <el-aside width="120px">
                <el-container direction="vertical">
                    <el-button type="primary">Symbol</el-button>
                    <el-button type="info" plain @click="getf">#</el-button>
                    <el-button type="plain" plain @click="gets">;</el-button>
                    <el-button type="info" plain @click="gett">:</el-button>
                    <el-button type="plain" plain @click="getfo">-></el-button>
                    <el-button type="info" plain @click="getfi">&lt;&gt;</el-button>
                    <el-button type="plain" plain @click="getsi">{}</el-button>
                    <el-button type="info" plain @click="getse">[]</el-button>
                    <el-button type="info" plain @click="gete">|</el-button>
                    <el-button type="plain" plain @click="getn">+</el-button>
                    <el-button type="info" plain @click="gette">@</el-button>
                    <!--            <el-button type="plain" plain @click="getev">Reset</el-button>-->
                </el-container>
            </el-aside>

            <el-container direction="vertical">
                <el-header>

                    <el-upload class="title"
                               name="file"
                               :action="fileUrl"
                               :show-file-list="false"
                               :on-success="first"
                               :before-upload="firstUp">
                        <el-button size="big" type="primary">Loading model file (xml)</el-button>
                    </el-upload>
                    <div class="title">
                        <!--              <el-button type="primary" class="title_name" @click="getev">ReSet</el-button>-->
                        <el-button type="primary" class="title_reset"><span ref="firstName">fileName</span></el-button>
                    </div>
                </el-header>
                <el-main v-show="upShowf==true">
                    <!--  <el-upload
                              name="file"
                              :action="fileUrl"
                              :show-file-list="false"
                              :on-success="first"
                              :before-upload="firstUp"
                      >
                        <el-button size="big" type="primary">load xml files</el-button>
                      </el-upload>-->
                    <div class="main_font">PreView</div>
                </el-main>

                <el-main v-if="vShowf==true">
                    <div id="first" class="first_v"></div>
                </el-main>
                <div ref="attr1">
                </div>
            </el-container>

            <el-container direction="vertical">
                <el-header class="second_select">
                    <el-upload class="title"
                               name="file"
                               :action="fileUrl"
                               :show-file-list="false"
                               :on-success="second"
                               :before-upload="secondUp"
                    >
                        <el-button size="big" type="primary">Loading model file (xml)</el-button>
                    </el-upload>
                    <div class="title">
                        <!--              <el-button type="primary" class="title_name" @click="gettw">ReSet</el-button>-->
                        <el-button type="primary" class="title_reset"><span ref="secondName">fileName</span></el-button>
                    </div>
                </el-header>
                <el-main v-show="upShows==true" class="seconds">
                    <div class="main_font">PreView</div>
                    <!--     <el-upload
                                 name="file"
                                 :action="fileUrl"
                                 :show-file-list="false"
                                 :on-success="second"
                                 :before-upload="secondUp"
                                 >
                           <el-button size="big" type="primary">upload xml file</el-button>
                         </el-upload>-->
                </el-main>

                <el-main v-if="vShows==true" class="seconds">
                    <div class="seconds_v" id="second" ref="vshow"></div>
                </el-main>
                <div ref="attr2">
                </div>


            </el-container>
            <!-- <el-aside width="120px">
                   <el-container direction="vertical">
                     <el-button type="primary" >Symbol</el-button>
                     <el-button type="info" plain @click="getf">#</el-button>
                     <el-button type="plain" plain @click="gets">;</el-button>
                     <el-button type="info" plain @click="gett">:</el-button>
                     <el-button type="plain" plain @click="getfo">-></el-button>
                     <el-button type="info" plain @click="getfi">&lt;&gt;</el-button>
                     <el-button type="plain" plain @click="getsi">{}</el-button>
                     <el-button type="info" plain @click="getse">[]</el-button>
                     <el-button type="plain" plain @click="gete">|</el-button>
                     <el-button type="info" plain @click="getn">+</el-button>
                     <el-button type="plain" plain @click="gette">@</el-button>
                     <el-button type="info"  plain @click="gettw">Reset</el-button>
                   </el-container>
             </el-aside>-->
        </el-container>

        <el-input id="input"
                  type="textarea"
                  :rows="4"
                  v-model="inputData"
                  placeholder="formulas input here.">
        </el-input>

        <el-footer height="60px">
            <el-button type="primary" @click="fuse">Combine</el-button>
            <el-button type="primary" @click="onDownload">Download</el-button>
            <el-button type="primary" @click="previewDialog = true">PreView</el-button>
        </el-footer>
    </el-container>
</template>

<script>
    import G6 from "@antv/g6";
    import axios from 'axios';
    /*import insertCss from 'insert-css';*/

    let myMap = new Map();

    // http://model.cherrytomatoes.cn:6789;
    const baseUrl = "http://localhost:6789";

    const fittingString = (str, maxWidth, fontSize) => {
        console.log(str + " " + maxWidth + " " + fontSize);
        let res = '';
        let array = str.split(' ');
        let j = 0;
        //if(array.length == 0) array.push(str);

        console.log(array);
        let retStr = [];
        for (var i in array) {
            let totalLength = 0;
            var tmpStr = array[i];
            let tmpArr = str.split('');
            for (j = 0; j < tmpArr.length; j++) {
                totalLength += G6.Util.getLetterWidth(tmpArr[j], fontSize);
                if (totalLength > maxWidth) {
                    tmpStr.substr(0, maxWidth - 4);
                    tmpStr += '..\n';
                    break;
                }
            }
            retStr.push(tmpStr)
            console.log(tmpStr)
        }
        for (var s in retStr) {
            res += retStr[s] + '\n';
        }
        console.log("Res:==>>" + res);
        return res;
    };



    ///uploadFile
    export default {
        name: 'Model',
        props: {
            msg: String
        },
        data() {
            return {
                inputData: '',
                upShowf: true,
                vShowf: false,
                upShows: true,
                vShows: false,
                fileUrl: baseUrl + '/uploadFile',
                filename: '',
                uploadUrl: '1',
                strJson: '',
                downFile: '',
                fileName: '',
                previewDialog: false,
                previewData: null
            }
        },
        methods: {

            drawTopo(dir, data) {
                //清理原数据
                if (myMap.get(dir) != null) {
                    myMap.get(dir).destroy();
                }

                let mWidth = 1000;
                if(dir != 'fuse'){
                    mWidth = 800;
                }

                const graphs = new G6.Graph({
                    container: dir,
                    width: mWidth,
                    height: 550,
                    fitView: true,
                    modes: {
                        default: [
                            // {
                            //     type: 'tooltip',
                            //     formatText(model) {
                            //         const text = 'label: ' + model.name
                            //         return text;
                            //     },
                            //     offset: 1
                            // },
                            'drag-canvas', 'drag-node', 'zoom-canvas',],
                    },
                    layout: {
                        type: 'dagre',
                        rankdir: 'LR',
                        align: 'DL',
                        nodesepFunc: () => 1,
                        ranksepFunc: () => 1,
                    },
                    defaultNode: {
                        size: [100, 40],
                        type: 'rect',
                        style: {
                            lineWidth: 2,
                            stroke: '#5B8FF9',
                            fill: '#C6E5FF',
                        },
                    },
                    defaultEdge: {
                        size: 1,
                        color: '#e37676',
                        style: {
                            endArrow: {
                                path: 'M 0,0 L 8,4 L 8,-4 Z',
                                fill: '#e2e2e2'
                            },
                        },
                    },
                });
                const globalFontSize = 12;
                graphs.node(function (node) {
                    console.log(node)
                    return {
                        label: fittingString(node.name, 120, globalFontSize),
                        labelCfg: {
                            style: {

                                position: 'left',
                                textAlign: 'center',
                                fontSize: 12
                            },
                        },
                    };
                });

                graphs.edge(function (edge) {
                    return {
                        label: fittingString(edge.linkType, 80, globalFontSize),
                        labelCfg: {
                            style: {
                                position: 'left',
                                textAlign: 'center',
                                fontSize: 12
                            },
                        },
                    };
                });

                graphs.on('node:click', evt => {
                    const item = evt.item; // 被操作的节点 item
                    const model = item.getModel();
                    let str = model.name;
                    if(model.attr != ''){
                        for(var a in model.attr)
                            str += ' {'+ model.attr[a] + '}';
                    }
                    if(dir == 'first')
                        this.$refs.attr1.innerHTML = str;
                    if(dir == 'second')
                        this.$refs.attr2.innerHTML = str;
                    if(dir == 'fuse')
                        this.$refs.attr3.innerHTML = str;
                });

                graphs.data(data);
                graphs.render();
                graphs.fitView();

                myMap.set(dir, graphs);
            },

            getf() {
                this.inputData += '#'
            },
            gets() {
                this.inputData += ';'
            },
            gett() {
                this.inputData += ':'
            },
            getfo() {
                this.inputData += '->'
            },
            getfi() {
                this.inputData += '<>'
            },
            getsi() {
                this.inputData += '{}'
            },
            getse() {
                this.inputData += '[]'
            },
            gete() {
                this.inputData += '|'
            },
            getn() {
                this.inputData += '+'
            },
            gette() {
                this.inputData += '@'
            },
            getev() {
                this.$refs.firstName.innerHTML = 'fileName';
                this.upShowf = true;
                this.vShowf = false;

            },
            gettw() {
                this.$refs.secondName.innerHTML = 'fileName';
                this.upShows = true;
                this.vShows = false;
            },
            firstUp(file) {
                const testmsg = file.name.substring(file.name.lastIndexOf(".") + 1);
                const isExcel = testmsg === 'xml';
                if (isExcel) {
                    return true;
                }
                this.$message.error('Loading model file (xml)');
                return false;
            },
            secondUp(file) {
                const testmsgs = file.name.substring(file.name.lastIndexOf(".") + 1);
                const isExcels = testmsgs === 'xml';
                if (isExcels) {
                    return true;
                }
                this.$message.error('Loading model file (xml)');
                return false;
            },

            //绘制模型1
            first(response) {
                this.upShowf = false;
                this.vShowf = true;
                this.filename_l = response.fileName;
                const data = JSON.parse(response.strJson);

                this.tempData = data;
                this.$refs.firstName.innerHTML = response.fileName;
                this.$nextTick(() => {
                    this.drawTopo('first', data);
                })
            },

            //绘制模型2
            second(response) {
                this.upShows = false;
                this.vShows = true;
                this.filename_r = response.fileName;
                const data = JSON.parse(response.strJson);
                this.tempData = data;
                this.$refs.secondName.innerHTML = response.fileName;
                this.$nextTick(() => {
                    this.drawTopo('second', data);
                })
            },

            //融合 http://model.cherrytomatoes.cn:6789/compile
            fuse() {
                const data = this.inputData;
                const fileName_l = this.filename_l;
                const fileName_r = this.filename_r;
                const url = baseUrl + '/compile';

                //没有公式直接返回
                if (this.inputData.length == 0) {
                    this.$message.error('The formula can`t be empty');
                    return;
                }

                axios.get(url, {       // 还可以直接把参数拼接在url后边
                    params: {
                        file1: fileName_l,
                        file2: fileName_r,
                        strReg: data
                    }
                }).then((e) => {
                    if (e.data.success == false) {
                        this.$message.error(e.data.message);
                        return;
                    }
                    this.$message.success("Combile success.");
                    this.uploadUrl = e.data.fileName;
                    this.previewData = JSON.parse(e.data.strJson);
                })
            },

            onDownload() {
                this.$prompt('Input FileName', 'Tips', {
                    confirmButtonText: 'OK',
                    cancelButtonText: 'Cancle',
                    inputValue: 'newXml'
                }).then(({value}) => {
                    if (this.filename_l == null || this.filename_r == null) {
                        console.log("model files needed!>>>>");
                        this.$message.error("Can not find model file ");
                        return;
                    }
                    this.fileName = value + '.xml',
                        this.$message({
                            type: 'success',
                            message: 'FileName: ' + value
                        });
                    this.fileDownLoad()
                }).catch(() => {
                    // this.fileName =  'newXml.xml'
                    // this.$message({
                    //   type: 'info',
                    //   message: '取消输入或者下载'
                    // });
                    // this.fileDownLoad()
                });
            },

            fileDownLoad() {
                console.log("Downloading.....");
                const fileName = this.uploadUrl;
                const url = baseUrl + '/downloadFile/' + fileName;

                console.log(url);
                axios.get(url, {       // 还可以直接把参数拼接在url后边
                    params: {}
                }).then((e) => {
                    if (e.data.success == false) {
                        this.$message.error("DownLoad Failed.")
                        return;
                    }
                    const content = e.data
                    const blob = new Blob([content]) // 构造一个blob对象来处理数据
                    if (this.fileName == undefined && this.fileName == '' && this.fileName == null) {
                        this.fileName = 'newXml.xml'
                    }
                    const fileName = this.fileName; // 导出文件名
                    // 对于<a>标签，只有 Firefox 和 Chrome（内核） 支持 download 属性
                    // IE10以上支持blob但是依然不支持download
                    if ('download' in document.createElement('a')) { // 支持a标签download的浏览器
                        const link = document.createElement('a') // 创建a标签
                        link.download = fileName // a标签添加属性
                        link.style.display = 'none'
                        link.href = URL.createObjectURL(blob)
                        document.body.appendChild(link)
                        link.click() // 执行下载
                        URL.revokeObjectURL(link.href) // 释放url
                        document.body.removeChild(link) // 释放标签
                    } else { // 其他浏览器
                        navigator.msSaveBlob(blob, fileName)
                    }
                    // this.btnSendTem = false
                }).catch((error) => {
                    console.log(error)
                    // 关闭loading
                    // this.loading = false
                    //this.btnSendTem = false
                })
            },

            openPreviewDialog() {
                console.log("openPreDialog");
                this.$nextTick(() => {
                    this.drawTopo("fuse", this.previewData);
                })
            },
            closePreviewDialog() {
                console.log("closePreDialog");
            }
        }
    }


</script>

<style>

    .el-header {
        background-color: papayawhip;
        color: #333;
        text-align: center;
        line-height: 60px;
    }

    .main_font {
        font-size: larger;
        color: #818181;
    }

    .title {
        display: inline-block;
        padding-left: 10px;
    }

    .title_reset {
        margin-right: 10px;
    }

    .second_select {
        background-color: powderblue;
        color: #333;
        text-align: center;
        line-height: 60px;
    }

    .el-footer {
        background-color: whitesmoke;
        color: #333;
        text-align: center;
        line-height: 60px;
    }


    .el-aside {
        background-color: #D3DCE6;
        color: #333;
        text-align: center;
        line-height: 560px;
    }

    .el-main {
        background-color: powderblue;
        color: #333;
        text-align: center;
        line-height: 600px;
    }

    .g6-tooltip {
        line-height: 20px;
        border-radius: 6px;
        font-size: 12px;
        color: #fff;
        background-color: #000;
        padding: 2px 8px;
        text-align: center;
    }


    .seconds {
        background-color: papayawhip;
        color: #333;
        text-align: center;
        line-height: 600px;
    }

    .seconds_v {
        background-color: papayawhip;
        color: #333;
        text-align: center;
        width: 100%;
        height: 600px;
    }

    .first_v {
        background-color: powderblue;
        color: #333;
        text-align: center;
        width: 100%;
        height: 600px;
    }

    body > .el-container {
        margin-bottom: 50px;
    }

    canvas {
        padding: 0px;
        margin: 0px;
        color: deepskyblue;

    }


    .el-container {
        padding: 0;
        margin: 0;
        width: 100%;
    }
</style>
