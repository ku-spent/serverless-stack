.PHONY: build clean deploy gomodgen

build: gomodgen
	export GO111MODULE=on
	env GOOS=linux go build -ldflags="-s -w" -o bin/getByUser recommendation/deliveries/lambda/getByUser/main.go

clean:
	rm -rf ./bin ./vendor go.sum

get:
	go mod download

deploy: clean get build
	sls deploy --verbose

gomodgen:
	chmod u+x gomod.sh
	./gomod.sh
