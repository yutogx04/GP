<template>
  <div class="signature-pad-container">
    <label v-if="label" class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
      {{ label }}
    </label>
    
    <div class="relative">
      <canvas 
        ref="canvas"
        @mousedown="startDrawing"
        @mousemove="draw"
        @mouseup="stopDrawing"
        @mouseleave="stopDrawing"
        @touchstart.prevent="startDrawingTouch"
        @touchmove.prevent="drawTouch"
        @touchend="stopDrawing"
        class="w-full h-40 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-800 cursor-crosshair"
      ></canvas>
      
      <!-- Controls -->
      <div class="flex gap-2 mt-2">
        <button @click="clear" type="button" class="text-sm text-slate-500 hover:text-slate-700 dark:hover:text-slate-300">
          Clear
        </button>
        <button @click="undo" type="button" class="text-sm text-slate-500 hover:text-slate-700 dark:hover:text-slate-300">
          Undo
        </button>
      </div>
    </div>
    
    <p v-if="isEmpty" class="mt-1 text-sm text-slate-500">Sign above</p>
    <p v-else class="mt-1 text-sm text-green-600">✓ Signature captured</p>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  label: { type: String, default: '' },
  modelValue: { type: String, default: '' },
  width: { type: Number, default: 400 },
  height: { type: Number, default: 160 }
})

const emit = defineEmits(['update:modelValue'])

const canvas = ref(null)
const ctx = ref(null)
const isDrawing = ref(false)
const isEmpty = ref(true)
const history = ref([])

onMounted(() => {
  const c = canvas.value
  c.width = props.width
  c.height = props.height
  ctx.value = c.getContext('2d')
  ctx.value.strokeStyle = '#1e293b'
  ctx.value.lineWidth = 2
  ctx.value.lineCap = 'round'
  ctx.value.lineJoin = 'round'
  
  // Load existing signature if any
  if (props.modelValue) {
    const img = new Image()
    img.onload = () => {
      ctx.value.drawImage(img, 0, 0)
      isEmpty.value = false
    }
    img.src = props.modelValue
  }
})

function getPosition(e, isTouch = false) {
  const rect = canvas.value.getBoundingClientRect()
  const clientX = isTouch ? e.touches[0].clientX : e.clientX
  const clientY = isTouch ? e.touches[0].clientY : e.clientY
  const scaleX = canvas.value.width / rect.width
  const scaleY = canvas.value.height / rect.height
  return {
    x: (clientX - rect.left) * scaleX,
    y: (clientY - rect.top) * scaleY
  }
}

function startDrawing(e) {
  saveHistory()
  isDrawing.value = true
  const pos = getPosition(e)
  ctx.value.beginPath()
  ctx.value.moveTo(pos.x, pos.y)
}

function startDrawingTouch(e) {
  saveHistory()
  isDrawing.value = true
  const pos = getPosition(e, true)
  ctx.value.beginPath()
  ctx.value.moveTo(pos.x, pos.y)
}

function draw(e) {
  if (!isDrawing.value) return
  const pos = getPosition(e)
  ctx.value.lineTo(pos.x, pos.y)
  ctx.value.stroke()
}

function drawTouch(e) {
  if (!isDrawing.value) return
  const pos = getPosition(e, true)
  ctx.value.lineTo(pos.x, pos.y)
  ctx.value.stroke()
}

function stopDrawing() {
  if (isDrawing.value) {
    isDrawing.value = false
    isEmpty.value = false
    emitSignature()
  }
}

function saveHistory() {
  history.value.push(canvas.value.toDataURL())
  if (history.value.length > 10) history.value.shift()
}

function undo() {
  if (history.value.length > 0) {
    const last = history.value.pop()
    const img = new Image()
    img.onload = () => {
      ctx.value.clearRect(0, 0, canvas.value.width, canvas.value.height)
      ctx.value.drawImage(img, 0, 0)
      emitSignature()
    }
    img.src = last
  }
}

function clear() {
  history.value = []
  ctx.value.clearRect(0, 0, canvas.value.width, canvas.value.height)
  isEmpty.value = true
  emit('update:modelValue', '')
}

function emitSignature() {
  const dataUrl = canvas.value.toDataURL('image/png')
  emit('update:modelValue', dataUrl)
}

// Expose methods for parent components
defineExpose({ clear, isEmpty })
</script>

<style scoped>
.signature-pad-container canvas {
  touch-action: none;
}
</style>
