int main(){
	int a = 0;
	int b = 1;
	int c = 5;
	int d = 10;

	if(a == b){
		c = c + 10;
		d = d + 5;
		if(c < b){
			b = c;
		}
		else if (c == b){
			c = d;
		}
		else{
			c = b;
		}
	}
	else if (a > b){
		c = c - 10;
		d = d - 5;
	}
	else{
		c = c + 10;
		d = d - 5;
	}

	return 0;
}
