/**
 * ============================================
 * 全局 Toast 通知工具
 * ============================================
 * 用法：
 *   import { useToast } from '@/utils/toast'
 *   const { toast } = useToast()
 *   toast('保存成功')        // info 默认
 *   toast('保存成功', 'success')
 *   toast('出错了', 'error')
 */

const TOAST_KEY = Symbol('toast')

let _toastFn = null

export function registerToast(fn) {
    _toastFn = fn
}

export function useToast() {
    function toast(message, type = 'info', duration = 2500) {
        if (_toastFn) {
            _toastFn(message, type, duration)
        }
    }
    return { toast }
}
