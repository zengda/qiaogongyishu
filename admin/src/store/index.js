import { createStore } from 'vuex'

export default createStore({
  state: {
    token: localStorage.getItem('admin_token') || '',
    user: null,
    sidebarCollapsed: false
  },
  getters: {
    token: state => state.token,
    user: state => state.user,
    sidebarCollapsed: state => state.sidebarCollapsed
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token
      localStorage.setItem('admin_token', token)
    },
    SET_USER(state, user) {
      state.user = user
    },
    SET_SIDEBAR_COLLAPSED(state, collapsed) {
      state.sidebarCollapsed = collapsed
    },
    LOGOUT(state) {
      state.token = ''
      state.user = null
      localStorage.removeItem('admin_token')
    }
  },
  actions: {
    login({ commit }, { token, user }) {
      commit('SET_TOKEN', token)
      commit('SET_USER', user)
    },
    logout({ commit }) {
      commit('LOGOUT')
    },
    toggleSidebar({ commit, state }) {
      commit('SET_SIDEBAR_COLLAPSED', !state.sidebarCollapsed)
    }
  }
})