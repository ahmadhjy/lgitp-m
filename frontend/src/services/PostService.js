import axios from 'axios';

const API_URL = 'http://localhost:8000/api/posts/';

class PostService {
  getPosts() {
    return axios.get(API_URL);
  }

  getPost(id) {
    return axios.get(`${API_URL}${id}/`);
  }

  createPost(post) {
    return axios.post(API_URL, post);
  }

  updatePost(id, post) {
    return axios.put(`${API_URL}${id}/`, post);
  }

  deletePost(id) {
    return axios.delete(`${API_URL}${id}/`);
  }
}

export default new PostService();
