<template>
  <div>
    <div class="menuDiv">
      <div>
        <h5>Данные (варианты ответов через запятую):</h5>
      </div>
      <div class="buttonAdd">
        <div style="margin-left: 10px;">
          <b-button variant="info" @click="addClick">Добавить</b-button>
        </div>
      </div>
    </div>
    <div>
      <label>Введите варианты ответов(названия через запятую):</label>
      <b-form-input
        v-model="addOrder.answer"
        id="textBDUpload"
        @change="changeAnswer"
        :state="!!addOrder.answer"
        placeholder="Введите варианты ответов через запятую"
        class="w-30 mb-2"
      />
      <ag-grid-vue
        :columnDefs="columnDefsFiles"
        :gridOptions="gridOptions"
        v-model="addOrder.dataManualFile"
        class="ag-theme-alpine h-100"
      />
    </div>
    <h5 v-if="!addOrder.dataManualFile.length" style="color: red;">
      Ведите данные!
    </h5>
    <h5 v-if="cellEmpty" style="color: red;">Введите данные в ячейки!</h5>
    <b-modal
      id="deletePhotoModal"
      title="Предупреждение"
      ok-title="Применить"
      cancel-title="Отмена"
      size="lg"
      @ok="deleteClick"
    >
      <div>
        Вы действительно хотите удалить строку данных?
      </div>
      <template v-slot:modal-footer="{ ok, cancel }">
        <b-button @click="ok()" variant="info">
          Удалить
        </b-button>
        <b-button @click="cancel()">
          Отмена
        </b-button>
      </template>
    </b-modal>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator'
import { AgGridVue } from 'ag-grid-vue'
import AgGridFactory from '@/factories/agGridFactory'
import ActionRenderer from '@/components/table/ActionRenderer.vue'
import { customerMapper } from '@/store/modules/customer'
import { GridApi } from 'ag-grid-community'

const Mapper = Vue.extend({
  computed: {
    ...customerMapper.mapState(['addOrder', 'flags'])
  },
  methods: {
    ...customerMapper.mapMutations([])
  }
})
@Component({
  components: {
    AgGridVue,
    ActionRenderer
  }
})
export default class PhotoInput extends Mapper {
  private deleteParams: any = null
  private gridApi: GridApi | null = null
  private cellEmpty = true
  private columnDefsFiles = [
    {
      headerName: 'Варианты ответов',
      placeholder: 'Названия через запятую',
      field: 'valueAnswer',
      colId: 'valueManualTitle'
    },
    {
      ...AgGridFactory.getActionColumn({
        cellRendererParams: {
          getActionByType: () => {
            return ['onLoad', 'onDelete', 'onClone'] //this.editable ? ['onDownload', 'onDelete'] : ['onDownload']
          },
          onLoad: this.onLoad,
          onDelete: this.onDelete,
          onClone: this.onClone
        },
        minWidth: 140,
        editable: false,
        maxWidth: 140
      })
    }
  ]
  private gridOptions = {
    ...AgGridFactory.getDefaultGridOptions(),
    domLayout: 'autoHeight',
    defaultColDef: {
      autoHeight: true,
      cellStyle: { 'white-space': 'normal' },
      editable: false
    },
    onGridReady: this.onGridReady,
    onCellValueChanged: this.onCellValueChanged
  }

  private onCellValueChanged(value: any) {
    this.cellEmpty = !value.data.fileValue || value.data.fileValue === ''
  }

  private onGridReady({ api }: { api: any }) {
    this.gridApi = api
  }

  private changeAnswer(newVal: string) {
    for (const item of this.addOrder.dataManualFile) {
      item.valueAnswer = newVal
    }
    this.gridApi?.setRowData(this.addOrder.dataManualFile)
  }

  private async onLoad(params: any) {
    this.addOrder.indexManual = params.rowIndex
    await document.getElementById('fileUpload')!.click()
  }

  @Watch('flags.filechange')
  onFileValueChange() {
    if (
      this.addOrder.indexManual !== -1 &&
      this.addOrder.indexManual !== null &&
      this.addOrder.indexManual !== undefined
    ) {
      this.cellEmpty = false
    }
  }

  private addClick() {
    this.addOrder.dataManualFile = this.addOrder.dataManualFile.concat({
      valueAnswer: this.addOrder.answer,
      fileValue: null
    })
    this.gridApi?.setRowData(this.addOrder.dataManualFile)
    this.cellEmpty = true
  }
  private onDelete(params: any) {
    this.deleteParams = params
    this.$bvModal.show('deletePhotoModal')
  }
  private deleteClick() {
    this.addOrder.dataManualFile = this.addOrder.dataManualFile.filter(
      (i: any, index: any) => index !== this.deleteParams.rowIndex
    )
  }
  onClone(params: any) {
    this.addOrder.dataManualFile = [
      ...this.addOrder.dataManualFile.filter(
        (i: any, index: any) => index <= params.rowIndex
      ),
      JSON.parse(
        JSON.stringify(
          this.addOrder.dataManualFile.find(
            (i: any, index: any) => index === params.rowIndex
          )
        )
      ),
      ...this.addOrder.dataManualFile.filter(
        (i: any, index: any) => index > params.rowIndex
      )
    ]
  }
}
</script>

<style scoped lang="scss">
@import '@/scss/_colors.scss';
.text-o-ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
}
.fieldSizeInput {
  margin-right: 2px;
}
.menuDiv {
  display: flex;
  padding: 10px;
}
.buttonAdd {
  margin: 0 0 0 auto;
}
</style>
