<template>
  <div>
    <p>Home page</p>
    <form onsubmit="return false">
		<br>
			Enter a long url:
			<input type="text" id="longUrl" name="longUrl">
		<br><br>
			<button @click="shorten">Create Short URL</button>
		<br>
			<p>Short URL: {{ shortUrl }}</p>
		<br>
	</form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      shortUrl: ''
    }
  },
  methods: {
    shorten() {
		this.shortUrl = this.shortenInBackend()
	},
	shortenInBackend() {
	  const path = `http://localhost:5000/api/shorten`
	  const longurl = document.getElementById('longUrl').value
	  axios.get(path, {
        params: {
          longUrl: longurl
        }
      })
      .then(response => {
        this.shortUrl = response.data.shortUrl
      })
      .catch(error => {
        console.log(error)
      })
    }
  }
}
</script>
