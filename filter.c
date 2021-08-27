#define KBUILD_MODNAME "filter"
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/udp.h>

struct Config {
    int should_drop;
    int source_port;
};
BPF_HASH(config, int, struct Config, 1);


/* Checks the config map and decides if we should drop packets */
static int should_drop(int source_port) {
    int zero = 0;
    struct Config *cfg = config.lookup(&zero);
    if (cfg == NULL) {
        return 0;
    }
    return cfg->should_drop && source_port == cfg->source_port;
}


int udpfilter(struct xdp_md *ctx) {
    // bpf_trace_printk("got a packet\n");
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;
    struct ethhdr *eth = data;

    if ((void*)eth + sizeof(*eth) > data_end) {
        return XDP_PASS;
    }

    struct iphdr *ip = data + sizeof(*eth);
    if ((void*)ip + sizeof(*ip) > data_end) {
        return XDP_PASS;
    }

    if (ip->protocol != IPPROTO_UDP) {
        return XDP_PASS;
    }

    struct udphdr *udp = (void*)ip + sizeof(*ip);
    if ((void*)udp + sizeof(*udp) > data_end) {
        return XDP_PASS;
    }

    if (should_drop(htons(udp->dest))) {
        return XDP_DROP;
    }

    return XDP_PASS;
}

